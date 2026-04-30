import os
import json
import re
from pathlib import Path

def parse_markdown_to_json(md_content, chapter_title):
    sections = []
    current_section = None
    
    # Pre-process lines to join broken sentences and multi-line titles
    raw_lines = md_content.split('\n')
    processed_lines = []
    
    for line in raw_lines:
        line = line.strip()
        if not line:
            processed_lines.append("")
            continue
            
        # Join logic: If the current line doesn't start with a header, list marker, or table marker
        last_non_empty_idx = len(processed_lines) - 1
        while last_non_empty_idx >= 0 and processed_lines[last_non_empty_idx] == "":
            last_non_empty_idx -= 1
            
        if last_non_empty_idx >= 0:
            prev = processed_lines[last_non_empty_idx]
            is_header = prev.startswith('#')
            # Check for list markers like (1), (a), (i) OR plain numbers like 1, 2 at start of line
            is_list_start = re.match(r'^(\(\d+\)|\d+\.|\d+\s+[A-Z]|\([a-z]\)|\([ivx]+\))', line)
            is_new_header = line.startswith('#')
            is_table_marker = line.startswith('|') or line.startswith('TABLE')
            
            # If the current line is NOT a new block (header, list, table)
            if not is_new_header and not is_list_start and not is_table_marker:
                # Merge if it was a header OR if the previous paragraph didn't end in punctuation
                # EXCEPT: Don't join if the current line starts with a number (likely a missed sub-point)
                if not re.match(r'^\d+\s+', line) and not prev.startswith('|') and not prev.startswith('TABLE') and (is_header or not re.search(r'[.:;]$', prev)):
                    # Remove intervening blank lines
                    while len(processed_lines) > last_non_empty_idx + 1:
                        processed_lines.pop()
                    processed_lines[last_non_empty_idx] = prev + " " + line
                    continue
        
        processed_lines.append(line)

    # Pattern for section headers: ### 1. Title.- or #### 49.1. Title .-
    section_pattern = re.compile(r'^#{3,4}\s+(\d+(?:\.\d+)?\s?[A-Z]?)\.\s+(.*)')
    
    i = 0
    while i < len(processed_lines):
        line = processed_lines[i].strip()
        if not line:
            i += 1
            continue
            
        # If it's a header line, try to match section pattern
        if line.startswith('#'):
            section_match = section_pattern.match(line)
            if section_match:
                number = section_match.group(1).strip()
                raw_title = section_match.group(2).strip()
                
                # Smart split: many titles end with separators followed by the paragraph text
                split_patterns = [r'\s+\.-\s+', r'\.-\s+', r'\s+\.\s?-\s+', r'\s+\.\s?–\s+', r'\s+\.\s?—\s+']
                split_done = False
                for pattern in split_patterns:
                    parts = re.split(pattern, raw_title, maxsplit=1)
                    if len(parts) == 2:
                        title, first_para = parts
                        title = title.strip(' .-–—')
                        current_section = {
                            "number": number,
                            "title": title,
                            "paragraphs": [first_para.strip()] if first_para.strip() else [],
                            "tables": []
                        }
                        split_done = True
                        break
                
                if not split_done:
                    current_section = {
                        "number": number,
                        "title": raw_title.strip(' .-–—'),
                        "paragraphs": [],
                        "tables": []
                    }
                sections.append(current_section)
                i += 1
                continue
            else:
                # If it's a header but doesn't match section pattern, just skip it (it's a chapter header)
                i += 1
                continue
            
        if not current_section:
            # If we haven't found a section yet, and there's text, 
            # create an "Introduction" section
            current_section = {
                "number": "0",
                "title": "Introduction",
                "paragraphs": [line],
                "tables": []
            }
            sections.append(current_section)
            i += 1
            continue

        # Check for table
        if line.startswith('|'):
            table_lines = []
            while i < len(processed_lines) and (processed_lines[i].strip().startswith('|') or (not processed_lines[i].strip() and i+1 < len(processed_lines) and processed_lines[i+1].strip().startswith('|'))):
                if not processed_lines[i].strip():
                    i += 1
                    continue
                table_lines.append(processed_lines[i].strip())
                i += 1
            
            if len(table_lines) >= 3:
                try:
                    sep_idx = -1
                    for idx, tl in enumerate(table_lines):
                        if re.match(r'^\|?\s*:?-+:?\s*(\|?\s*:?-+:?\s*)*\|?$', tl):
                            sep_idx = idx
                            break
                    
                    if sep_idx != -1:
                        headers = []
                        for h_line in table_lines[:sep_idx]:
                            h_cols = [c.strip() for c in h_line.split('|')]
                            if h_line.startswith('|'): h_cols = h_cols[1:]
                            if h_line.endswith('|'): h_cols = h_cols[:-1]
                            if not headers:
                                headers = h_cols
                            else:
                                for j in range(min(len(headers), len(h_cols))):
                                    if h_cols[j]:
                                        headers[j] = (headers[j] + " " + h_cols[j]).strip()
                        
                        rows = []
                        for row_line in table_lines[sep_idx+1:]:
                            row_data = [c.strip() for c in row_line.split('|')]
                            if row_line.startswith('|'): row_data = row_data[1:]
                            if row_line.endswith('|'): row_data = row_data[:-1]
                            rows.append([c.strip() for c in row_data])
                        
                        table_title = "Table"
                        if current_section["paragraphs"]:
                            for p_idx in range(len(current_section["paragraphs"])-1, -1, -1):
                                prev_p = current_section["paragraphs"][p_idx]
                                title_match = re.search(r'(Table\s+\d+[:\s][^.]*)', prev_p, re.I)
                                if title_match:
                                    table_title = title_match.group(1).strip()
                                    if len(prev_p) < len(table_title) + 5:
                                        current_section["paragraphs"].pop(p_idx)
                                    break
                        
                        current_section["tables"].append({
                            "title": table_title,
                            "headers": headers,
                            "rows": rows
                        })
                except Exception as e:
                    print(f"Warning: Failed to parse table in {chapter_title}: {e}")
            continue

        # Otherwise it's a paragraph
        current_section["paragraphs"].append(line)
        i += 1
                
    return {
        "title": chapter_title,
        "sections": sections
    }

def process_rule(rule_id, rule_name):
    base_dir = Path("/Users/cyrilckurian/Desktop/Kerala-map")
    rules_dir = base_dir / "data" / "building_rules" / rule_id
    json_path = base_dir / "web-app" / "src" / "lib" / "data" / f"{rule_id}.json"
    
    if not rules_dir.exists():
        print(f"Error: {rules_dir} not found")
        return

    existing_data = {}
    if json_path.exists():
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            pass
            
    md_files = sorted(list(rules_dir.glob("chapter_*.md")))
    
    new_content = {}
    new_chapters = []
    
    for md_file in md_files:
        match = re.search(r'chapter_(\d+)', md_file.name)
        if not match:
            continue
            
        chapter_num = int(match.group(1))
        chapter_id = f"chapter-{chapter_num}"
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        title_match = re.search(r'^#\s+(.*)', content)
        full_title = title_match.group(1).strip() if title_match else md_file.stem
        if ' — ' in full_title:
            chapter_title = full_title.split(' — ', 1)[1].strip()
        elif re.match(r'^Chapter\s+\d+:\s+', full_title, re.I):
            chapter_title = re.sub(r'^Chapter\s+\d+:\s+', '', full_title, flags=re.I).strip()
        else:
            chapter_title = full_title
        
        content = re.sub(r'^\s*This is a digitally signed Gazette\..*$', '', content, flags=re.M | re.I)
        content = re.sub(r'^\s*Authenticity may be verified through https://compose\.kerala\.gov\.in/.*$', '', content, flags=re.M | re.I)
        content = re.sub(r'^\s*KERALA MUNICIPALITY BUILDING RULES.*$', '', content, flags=re.M | re.I)

        parsed_chapter = parse_markdown_to_json(content, chapter_title)
        new_content[chapter_id] = parsed_chapter
        
        existing_chapter = next((c for c in existing_data.get("chapters", []) if c["id"] == chapter_id), None)
        icon = existing_chapter["icon"] if existing_chapter and "icon" in existing_chapter else "description"
        
        new_chapters.append({
            "id": chapter_id,
            "number": chapter_num,
            "title": chapter_title,
            "icon": icon
        })
        
    result_data = {
        "id": rule_id,
        "name": rule_name,
        "lastUpdated": "Apr 2026",
        "chapters": new_chapters,
        "content": new_content
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully updated {json_path} with {len(new_chapters)} chapters.")

def main():
    process_rule("kmbr", "Kerala Municipality Building Rules (1999)")
    process_rule("kpbr", "Kerala Panchayat Building Rules (2019)")

if __name__ == "__main__":
    main()
