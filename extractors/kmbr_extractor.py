"""
KMBR Extractor — Kerala Municipal Building Rules
Scrapes each chapter from https://lsgkerala.gov.in/htm/kmbr/ and saves
one markdown file per chapter.

Approach
--------
The KMBR pages use HTML <table> elements purely for page layout (no <th>).
Instead of trying to parse the element tree, we:
  1. Replace real data tables (those with <th>) with placeholders.
  2. Replace <br> with newlines and add newlines around <p> blocks.
  3. Extract the resulting plain text.
  4. Re-join "continuation" lines (indented, non-structural).
  5. Classify each merged line and emit proper Markdown.

Heading hierarchy
-----------------
# Chapter N: Title          ← our own chapter-level H1
## CHAPTER N DEFINITIONS    ← from the HTML chapter heading
### N. Rule title            ← numbered rule
**( N )** Sub-rule text      ← numbered sub-rule (1), (2), …
- **(a)** Definition text    ← lettered definition item
  - **(i)** Sub-item text    ← roman-numeral or nested lettered sub-item
"""

import os
import re
import time

import requests
from bs4 import BeautifulSoup

CHAPTER_BASE_URL = "https://lsgkerala.gov.in/htm/kmbr/"

CHAPTERS = [
    (1,  "Definitions"),
    (2,  "Permit"),
    (3,  "Action Against Unauthorized Constructions"),
    (4,  "General Provisions Regarding Site and Building"),
    (5,  "Occupancy"),
    (6,  "Parts of Building"),
    (7,  "Special Provisions for Certain Occupancy"),
    (8,  "Buildings in Small Plots"),
    (9,  "Row Buildings"),
    (10, "Building Construction Under Approved Schemes"),
    (11, "Construction in Plots Surrendered for Roads"),
    (12, "Accessory Buildings and Sheds"),
    (13, "Conversion of Roof and Shutters"),
    (14, "Wall and Fence"),
    (15, "Special Provisions for Certain Constructions"),
    (16, "Wells"),
    (17, "Safety Provisions for High Rise Buildings"),
    (18, "Huts"),
    (19, "Telecommunication Towers"),
    (20, "Regularisation of Unpermitted Constructions"),
    (21, "Registration of Architects, Engineers, Planners"),
    (22, "Art and Heritage Commission"),
    (23, "Vigilance, Dangerous Works, Appeals"),
]

# Roman numerals used as sub-items (i), (ii), (iii) … inside definitions
_ROMAN = frozenset([
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix",
    "x", "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii",
    "xix", "xx",
])

# Patterns that signal "start of a new structural element"
_STRUCTURAL = [
    re.compile(r"^\(\d+\)\s"),                  # (1), (2), (3) …
    re.compile(r"^\([a-zA-Z]+\)\s"),             # (a), (b), (ia) …
    re.compile(r"^\d+\.\s"),                     # 1. 2. 3. …
    re.compile(r"^CHAPTER\s+\d+", re.I),
    re.compile(r"^SCHEDULE\b", re.I),
    re.compile(r"^Note\s*[:-]", re.I),
    re.compile(r"^Provided\s+that", re.I),
    re.compile(r"^RULES$"),
    re.compile(r"^NOTES$"),
]

_TABLE_PH = re.compile(r"^__TABLE_\d+__$")


# ---------------------------------------------------------------------------
# Network helpers
# ---------------------------------------------------------------------------

def _fetch(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding or "utf-8"
            return r.text
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    return ""


# ---------------------------------------------------------------------------
# Data-table detection and conversion
# ---------------------------------------------------------------------------

def _is_data_table(table) -> bool:
    """
    True if this table contains data (not a page-layout wrapper).
    KMBR layout tables always have border=0.
    Data tables have border>0.
    """
    # Exclude hidden tables (tooltips/popups)
    curr = table
    while curr:
        style = curr.get("style", "")
        if isinstance(style, str) and re.search(r"(visibility:\s*hidden|display:\s*none)", style, re.I):
            return False
        curr = curr.parent

    if table.find("th"):
        return True
    try:
        if int(table.get("border", 0)) > 0:
            return True
    except (ValueError, TypeError):
        pass
    return False


def _table_to_md(table) -> str:
    """Convert a data <table> to a Markdown table string."""
    rows = table.find_all("tr")
    if not rows:
        return ""
        
    # First pass: find dimensions
    max_cols = 0
    for row in rows:
        cells = row.find_all(["td", "th"])
        cols = 0
        for cell in cells:
            cols += int(cell.get("colspan", 1))
        max_cols = max(max_cols, cols)
        
    if max_cols == 0:
        return ""
        
    grid = [["" for _ in range(max_cols)] for _ in range(len(rows))]
    
    for r_idx, row in enumerate(rows):
        cells = row.find_all(["td", "th"])
        c_idx = 0
        for cell in cells:
            while c_idx < max_cols and grid[r_idx][c_idx] != "":
                c_idx += 1
            if c_idx >= max_cols:
                break
                
            colspan = int(cell.get("colspan", 1))
            rowspan = int(cell.get("rowspan", 1))
            
            # Extract text
            text = re.sub(r"\s+", " ", cell.get_text(separator=" ")).strip().replace("|", "\\|")
            
            for r in range(rowspan):
                for c in range(colspan):
                    if r_idx + r < len(grid) and c_idx + c < max_cols:
                        grid[r_idx + r][c_idx + c] = text
                        
            c_idx += colspan

    # Remove title rows (where all cells are the same)
    filtered_grid = []
    for r_idx, row in enumerate(grid):
        distinct = set(c for c in row if c)
        if len(distinct) == 1 and row[0] != "":
            continue # Skip title row
        filtered_grid.append(row)
        
    if not filtered_grid:
        return ""

    header_depth = 1
    first_non_title_row_idx = len(grid) - len(filtered_grid)
    if first_non_title_row_idx < len(rows):
        first_row = rows[first_non_title_row_idx]
        for cell in first_row.find_all(["td", "th"]):
            rs = int(cell.get("rowspan", 1))
            if rs > header_depth:
                header_depth = rs

    # Merge the first `header_depth` rows into a single header row
    if header_depth > 1 and header_depth <= len(filtered_grid):
        merged_header = []
        for c in range(max_cols):
            # deduplicate adjacent identical text vertically
            parts = []
            for r in range(header_depth):
                val = filtered_grid[r][c]
                if not parts or val != parts[-1]:
                    parts.append(val)
            merged_header.append(" <br> ".join(parts).strip())
            
        # Replace the first `header_depth` rows with this single merged row
        filtered_grid = [merged_header] + filtered_grid[header_depth:]
        
    md_rows = []
    for i, row in enumerate(filtered_grid):
        md_rows.append("| " + " | ".join(row) + " |")
        if i == 0:
            md_rows.append("| " + " | ".join(["---"] * max_cols) + " |")
            
    return "\n".join(md_rows)


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def _extract_text(html: str) -> tuple[str, dict[str, str]]:
    """
    Return (plain_text_with_newlines, {placeholder: markdown_table}).
    Data tables are replaced by __TABLE_N__ placeholders.
    """
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    # Replace real data tables with placeholders
    data_tables: dict[str, str] = {}
    for i, tbl in enumerate(soup.find_all("table")):
        if _is_data_table(tbl):
            ph = f"__TABLE_{i}__"
            md = _table_to_md(tbl)
            data_tables[ph] = md
            tbl.replace_with(f"\n\n{ph}\n\n")

    # <br> → newline
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Wrap block elements so get_text produces natural paragraph breaks
    for tag in soup.find_all(["p", "div", "tr", "li"]):
        tag.insert_before("\n")
        tag.insert_after("\n")

    body = soup.find("body") or soup
    raw = body.get_text(separator="")
    return raw, data_tables


# ---------------------------------------------------------------------------
# Line classification (applied AFTER merging continuations)
# ---------------------------------------------------------------------------

def _is_structural(text: str) -> bool:
    return any(p.match(text) for p in _STRUCTURAL) or _TABLE_PH.match(text) is not None


def _classify(text: str) -> str:
    """Return the semantic type of a merged line."""
    if _TABLE_PH.match(text):
        return "table_ph"
    if re.match(r"^CHAPTER\s+\d+", text, re.I):
        return "chapter"
    if re.match(r"^SCHEDULE\b", text, re.I):
        return "chapter"
    if re.match(r"^\d+\.\s+\S", text):
        return "rule"
    if re.match(r"^Note\s*[:-]", text, re.I):
        return "note"
    if re.match(r"^Provided\s+that", text, re.I):
        return "provided"
    if text in ("RULES", "NOTES"):
        return "section_header"

    # Parenthesised letter key — (a), (b), (ia), (aa) …
    m_letter = re.match(r"^\(([a-zA-Z]+)\)", text)
    if m_letter:
        letters = m_letter.group(1).lower()
        rest    = text[m_letter.end():].strip()
        # Definition items always open with a single-quoted term: (a) 'access' …
        # Roman sub-items never do (they list things like "(i) garden, …")
        if rest.startswith("'"):
            return "def_item"
        # Roman numerals are ALWAYS nested sub-items, regardless of HTML indentation.
        # In every chapter a bare (i)/(ii)/… without a quoted term is a sub-point
        # under some parent letter or uppercase-letter item.
        if letters in _ROMAN:
            return "sub_item"
        return "def_item"

    # Parenthesised digit — (1), (2), (3) …
    m_digit = re.match(r"^\((\d+)\)", text)
    if m_digit:
        rest = text[m_digit.end():].strip()
        # In the source HTML the letter 'l' is sometimes rendered as digit '1'.
        # If the content starts with a single quote it's a definition item (l).
        if rest.startswith("'"):
            return "def_item"
        return "subrule"

    return "body"


# ---------------------------------------------------------------------------
# Text → structured lines
# ---------------------------------------------------------------------------

_ORPHAN_RE = re.compile(r"^['\"‘’“”\s]+$")  # lone quote artifacts

def _parse_text(raw: str) -> list[tuple[bool, str]]:
    """
    Return list of (has_leading_whitespace, stripped_text) for non-empty lines.
    &nbsp; / \xa0 are normalised to regular spaces first.
    Lines that are nothing but orphaned quote characters are dropped.
    """
    result: list[tuple[bool, str]] = []
    for line in raw.split("\n"):
        line = line.replace("\xa0", " ")
        indented = line != line.lstrip()
        line_clean = re.sub(r"\s+", " ", line).strip()
        if line_clean and not _ORPHAN_RE.match(line_clean):
            result.append((indented, line_clean))
    return result


def _merge_continuations(lines: list[tuple[bool, str]]) -> list[tuple[bool, str]]:
    """
    Join indented non-structural lines onto the previous line.
    An indented line that starts with a structural marker is NOT a continuation.
    """
    merged: list[tuple[bool, str]] = []
    for indented, text in lines:
        if indented and not _is_structural(text) and merged:
            prev_ind, prev_text = merged[-1]
            merged[-1] = (prev_ind, prev_text + " " + text)
        else:
            merged.append((indented, text))
    return merged


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def _to_markdown(
    lines: list[tuple[bool, str]],
    chapter_num: int,
    chapter_title: str,
    data_tables: dict[str, str],
) -> str:
    out: list[str] = [f"# Chapter {chapter_num}: {chapter_title}", ""]
    prev_type = "body"

    for indented, text in lines:
        ltype = _classify(text)

        # When leaving a subrule group, close it with a blank line
        if prev_type == "subrule" and ltype != "subrule":
            out.append("")

        if ltype == "section_header":
            out += ["", f"## {text}", ""]

        elif ltype == "chapter":
            out += ["", f"## {text}", ""]

        elif ltype == "rule":
            out += ["", f"### {text}", ""]

        elif ltype == "subrule":
            m = re.match(r"\((\d+)\)", text)
            num = m.group(1)
            rest = text[m.end():].strip()
            # Blank line before the first item of a new ordered list
            if prev_type != "subrule":
                out.append("")
            # Emit as a proper ordered-list item: "1. text"
            out.append(f"{num}. {rest}")

        elif ltype == "def_item":
            # Key may be letters (a) or a digit confused with a letter, e.g. (1) = (l)
            m = re.match(r"\(([a-zA-Z\d]+)\)", text)
            key_inner = m.group(1)
            rest = text[m.end():].strip()
            # Digit '1' in a definition context is the letter 'l' in the source doc
            if key_inner.isdigit():
                key_inner = "l"
            out.append(f"- **({key_inner})** {rest}")

        elif ltype == "sub_item":
            m = re.match(r"\(([a-zA-Z]+)\)", text)
            key_inner = m.group(1)
            rest = text[m.end():].strip()
            out.append(f"  - **({key_inner})** {rest}")

        elif ltype == "note":
            body = re.sub(r"^Note\s*[:-]\s*", "", text, flags=re.I)
            out.append(f"> **Note:** {body}")

        elif ltype == "provided":
            out.append(f"> {text}")

        elif ltype == "table_ph":
            ph = text.strip()
            if ph in data_tables:
                out += ["", data_tables[ph], ""]

        else:  # body
            out += [text, ""]

        prev_type = ltype

    # Collapse runs of more than one blank line
    cleaned: list[str] = []
    blank_run = 0
    for line in out:
        if line.strip() == "":
            blank_run += 1
            if blank_run == 1:
                cleaned.append("")
        else:
            blank_run = 0
            cleaned.append(line)

    return "\n".join(cleaned).strip() + "\n"


# ---------------------------------------------------------------------------
# Per-chapter pipeline
# ---------------------------------------------------------------------------

def _parse_chapter(html: str, chapter_num: int, chapter_title: str) -> str:
    raw, data_tables = _extract_text(html)
    lines = _parse_text(raw)
    lines = _merge_continuations(lines)
    return _to_markdown(lines, chapter_num, chapter_title, data_tables)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def _safe_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*,]', "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:80].lower()


def extract_kmbr(output_dir: str) -> None:
    """Fetch all 23 KMBR chapters and write one .md file per chapter."""
    os.makedirs(output_dir, exist_ok=True)

    for num, title in CHAPTERS:
        url = f"{CHAPTER_BASE_URL}kmbr_chapter{num}.html"
        print(f"  Chapter {num:2d}: {title}")
        try:
            html = _fetch(url)
            md   = _parse_chapter(html, num, title)

            filename = f"chapter_{num:02d}_{_safe_filename(title)}.md"
            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as fh:
                fh.write(md)

            print(f"           -> {filename}  ({len(md):,} chars)")
            time.sleep(0.4)
        except Exception as exc:
            print(f"           ERROR: {exc}")
