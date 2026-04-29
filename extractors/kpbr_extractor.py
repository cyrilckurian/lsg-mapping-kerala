"""
KPBR Extractor — Kerala Panchayat Building Rules 2019
Downloads the official PDF and converts each chapter to a separate markdown file.
Uses PyMuPDF (fitz) for layout-aware text and table extraction.
"""

import os
import re

import fitz  # PyMuPDF
import requests

PDF_URL = (
    "https://buildingpermit.lsgkerala.gov.in/Content/Rules/2019_kpbr.pdf"
)

# Patterns that signal a chapter boundary — case-sensitive to avoid matching
# inline references like "Schedule III" or "chapter XVI" in body text
_CHAPTER_RE  = re.compile(r"^CHAPTER\s+([IVX]+|\d+)\b")
_SCHEDULE_RE = re.compile(r"^SCHEDULE\s+([IVX]+|\d+)\b")

# Chapter subtitle: a short all-caps line immediately after a chapter heading
_SUBTITLE_RE = re.compile(r"^[A-Z][A-Z ,/\-&()]+$")

# Digitally-signed Gazette boilerplate that appears at the bottom of every page
_GAZETTE_RE  = re.compile(r"This is a digitally signed Gazette|compose\.kerala\.gov\.in|Authenticity may be verified")

# Patterns for rule / sub-rule classification (body text)
_RULE_RE     = re.compile(r"^\d+\.\s+\S")
_SUBRULE_RE  = re.compile(r"^\(\d+\)\s")
_SUBITEM_RE  = re.compile(r"^\([a-zA-Z]+\)\s")


# ---------------------------------------------------------------------------
# Download helper
# ---------------------------------------------------------------------------

def _download_pdf(url: str, dest: str) -> None:
    print(f"  Downloading KPBR PDF …")
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    total = int(r.headers.get("content-length", 0))
    done  = 0
    with open(dest, "wb") as fh:
        for chunk in r.iter_content(65536):
            fh.write(chunk)
            done += len(chunk)
    print(f"  Downloaded {done:,} bytes → {dest}")


# ---------------------------------------------------------------------------
# Font / layout helpers
# ---------------------------------------------------------------------------

def _median_font_size(doc: fitz.Document) -> float:
    sizes: list[float] = []
    for page in doc:
        for blk in page.get_text("dict").get("blocks", []):
            if blk.get("type") != 0:
                continue
            for ln in blk.get("lines", []):
                for sp in ln.get("spans", []):
                    sz = sp.get("size", 0.0)
                    if sz > 0:
                        sizes.append(sz)
    if not sizes:
        return 12.0
    sizes.sort()
    return sizes[len(sizes) // 2]


def _is_bold(span: dict) -> bool:
    flags = span.get("flags", 0)
    font  = span.get("font", "")
    return bool(flags & 16) or "Bold" in font or "bold" in font


def _heading_level(text: str, size: float, bold: bool, body: float) -> int:
    """Return markdown heading level (1-4) or 0 for body text."""
    text = text.strip()
    if _CHAPTER_RE.match(text) or _SCHEDULE_RE.match(text):
        return 1
    if size >= body * 1.45 and bold:
        return 2
    if size >= body * 1.2 and bold:
        return 3
    if bold and _RULE_RE.match(text):
        return 3
    if bold and size >= body * 1.05:
        return 4
    return 0


# ---------------------------------------------------------------------------
# Table extraction
# ---------------------------------------------------------------------------

def _table_to_md(data: list[list]) -> str:
    if not data:
        return ""
    rows: list[str] = []
    for i, row in enumerate(data):
        cells = [
            re.sub(r"\s+", " ", str(c or "")).strip().replace("|", "\\|")
            for c in row
        ]
        rows.append("| " + " | ".join(cells) + " |")
        if i == 0:
            rows.append("| " + " | ".join(["---"] * len(cells)) + " |")
    return "\n".join(rows)


def _page_table_bboxes(page: fitz.Page) -> list[tuple]:
    """Return list of (bbox, markdown_string) for every table on the page."""
    results: list[tuple] = []
    try:
        for tbl in page.find_tables():
            md = _table_to_md(tbl.extract())
            if md and tbl.bbox:
                results.append((fitz.Rect(tbl.bbox), md))
    except Exception:
        pass
    return results


def _in_any_table(block_rect: fitz.Rect, table_rects: list[tuple]) -> bool:
    for (trect, _) in table_rects:
        if trect.intersects(block_rect):
            return True
    return False


# ---------------------------------------------------------------------------
# PDF → chapter list
# ---------------------------------------------------------------------------

class _Block:
    __slots__ = ("kind", "level", "text")

    def __init__(self, kind: str, level: int, text: str):
        self.kind  = kind   # "heading" | "body" | "table"
        self.level = level
        self.text  = text


def _process_pdf(pdf_path: str) -> list[dict]:
    """
    Return a list of chapter dicts:
        {"title": str, "blocks": list[_Block]}
    """
    doc   = fitz.open(pdf_path)
    body  = _median_font_size(doc)
    print(f"  Body font size ≈ {body:.1f}pt")

    chapters: list[dict] = []
    cur_title: str | None = None
    cur_blocks: list[_Block] = []
    expecting_subtitle = False  # True immediately after a chapter/schedule heading

    for page_num, page in enumerate(doc):
        tables = _page_table_bboxes(page)

        # Insert table blocks sorted by vertical position
        pending_tables = sorted(tables, key=lambda t: t[0].y0)
        table_inserted = [False] * len(pending_tables)

        page_dict = page.get_text("dict", sort=True)

        for blk in page_dict.get("blocks", []):
            if blk.get("type") != 0:
                continue

            blk_rect = fitz.Rect(blk.get("bbox", [0, 0, 0, 0]))

            # Skip text that belongs to a detected table
            if _in_any_table(blk_rect, tables):
                # Flush pending table that starts before this block
                for ti, (trect, tmd) in enumerate(pending_tables):
                    if not table_inserted[ti] and trect.y0 <= blk_rect.y0:
                        b = _Block("table", 0, tmd)
                        if cur_title is None:
                            cur_blocks.append(b)
                        else:
                            cur_blocks.append(b)
                        table_inserted[ti] = True
                continue

            # Flush tables that appear above this block
            for ti, (trect, tmd) in enumerate(pending_tables):
                if not table_inserted[ti] and trect.y0 <= blk_rect.y0:
                    b = _Block("table", 0, tmd)
                    cur_blocks.append(b)
                    table_inserted[ti] = True

            # Combine spans in the same line → single text run
            for ln in blk.get("lines", []):
                spans = ln.get("spans", [])
                if not spans:
                    continue

                line_text = " ".join(s.get("text", "") for s in spans).strip()
                line_text = re.sub(r"\s+", " ", line_text)
                if not line_text:
                    continue

                # Drop Gazette boilerplate that appears at the bottom of every page
                if _GAZETTE_RE.search(line_text):
                    continue

                dom = max(spans, key=lambda s: s.get("size", 0))
                sz  = dom.get("size", body)
                bold = _is_bold(dom)

                level = _heading_level(line_text, sz, bold, body)

                # Chapter / Schedule boundary → start new chapter
                if level == 1:
                    if cur_title is not None:
                        chapters.append({"title": cur_title, "blocks": cur_blocks})
                    cur_title  = line_text
                    cur_blocks = []
                    expecting_subtitle = True
                elif expecting_subtitle:
                    # Line immediately after a chapter heading may be its subtitle
                    # (e.g. "DEFINITIONS" after "CHAPTER I")
                    if bold and _SUBTITLE_RE.match(line_text) and not _RULE_RE.match(line_text):
                        cur_title = f"{cur_title} — {line_text}"
                    else:
                        if level > 0:
                            cur_blocks.append(_Block("heading", level, line_text))
                        else:
                            cur_blocks.append(_Block("body", 0, line_text))
                    expecting_subtitle = False
                elif level > 0:
                    cur_blocks.append(_Block("heading", level, line_text))
                else:
                    cur_blocks.append(_Block("body", 0, line_text))

        # Flush any remaining tables on this page
        for ti, (trect, tmd) in enumerate(pending_tables):
            if not table_inserted[ti]:
                cur_blocks.append(_Block("table", 0, tmd))

    if cur_title is not None:
        chapters.append({"title": cur_title, "blocks": cur_blocks})

    doc.close()
    return chapters


# ---------------------------------------------------------------------------
# Chapter → Markdown
# ---------------------------------------------------------------------------

def _chapter_to_md(chapter: dict) -> str:
    title  = chapter["title"]
    blocks = chapter["blocks"]

    lines: list[str] = [f"# {title}", ""]

    # Accumulate body text into paragraphs; flush on heading/table
    para: list[str] = []

    def flush_para() -> None:
        if not para:
            return
        full = " ".join(para).strip()
        if not full:
            para.clear()
            return

        # Split on sub-rule / sub-item boundaries to preserve indentation
        segments = re.split(r"(?=\(\d+\)\s|\([a-zA-Z]+\)\s)", full)
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            if _SUBRULE_RE.match(seg) or _SUBITEM_RE.match(seg):
                lines.append(f"  {seg}")
            else:
                lines.append(seg)
        lines.append("")
        para.clear()

    for blk in blocks:
        if blk.kind == "heading":
            flush_para()
            lines.append(f"{'#' * (blk.level + 1)} {blk.text}")
            lines.append("")
        elif blk.kind == "table":
            flush_para()
            lines.append(blk.text)
            lines.append("")
        else:  # body
            para.append(blk.text)

    flush_para()

    # Collapse multiple consecutive blank lines
    cleaned: list[str] = []
    blank_run = 0
    for ln in lines:
        if ln.strip() == "":
            blank_run += 1
            if blank_run == 1:
                cleaned.append("")
        else:
            blank_run = 0
            cleaned.append(ln)

    return "\n".join(cleaned).strip() + "\n"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def _safe_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\[\],]', "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:80].lower()


def extract_kpbr(output_dir: str, pdf_path: str | None = None) -> None:
    """Download the KPBR 2019 PDF and write one .md file per chapter."""
    os.makedirs(output_dir, exist_ok=True)

    if pdf_path is None:
        pdf_path = os.path.join(output_dir, "_kpbr_2019.pdf")

    if not os.path.exists(pdf_path):
        _download_pdf(PDF_URL, pdf_path)
    else:
        print(f"  Using cached PDF: {pdf_path}")

    print("  Analysing PDF structure …")
    chapters = _process_pdf(pdf_path)

    if not chapters:
        print("  WARNING: no chapters detected — check the PDF layout.")
        return

    print(f"  Found {len(chapters)} chapter(s)")

    for i, chapter in enumerate(chapters, 1):
        title    = chapter["title"]
        md       = _chapter_to_md(chapter)
        filename = f"chapter_{i:02d}_{_safe_filename(title)}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(md)

        print(f"  Chapter {i:2d}: {title[:55]:<55} -> {filename}")
