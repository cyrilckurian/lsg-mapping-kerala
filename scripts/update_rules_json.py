import os
import json
import re
from pathlib import Path

def parse_markdown_to_json(md_content, chapter_title):
    sections = []
    current_section = None
    
    lines = md_content.split('\n')
    
    # Pattern for section headers: ### 1. Title.- or #### 1. Title .-
    section_pattern = re.compile(r'^#{3,4}\s+(\d+[A-Z]?)\.\s+(.*)')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
            
        section_match = section_pattern.match(line)
        if section_match:
            number = section_match.group(1)
            title = section_match.group(2).strip(' .-')
            current_section = {
                "number": number,
                "title": title,
                "paragraphs": [],
                "tables": []
            }
            sections.append(current_section)
            i += 1
            continue
            
        if not current_section:
            i += 1
            continue

        # Check for table
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            
            if len(table_lines) >= 3:
                try:
                    headers = [c.strip() for c in table_lines[0].split('|') if c.strip()]
                    rows = []
                    for row_line in table_lines[2:]:
                        row_data = [c.strip() for c in row_line.split('|')]
                        if row_line.startswith('|'): row_data = row_data[1:]
                        if row_line.endswith('|'): row_data = row_data[:-1]
                        rows.append([c.strip() for c in row_data])
                    
                    table_title = "Table"
                    if current_section["paragraphs"]:
                        prev_p = current_section["paragraphs"][-1]
                        title_match = re.search(r'(Table\s+\d+[:\s][^.]*)', prev_p)
                        if title_match:
                            table_title = title_match.group(1).strip()
                    
                    current_section["tables"].append({
                        "title": table_title,
                        "headers": headers,
                        "rows": rows
                    })
                except Exception as e:
                    print(f"Warning: Failed to parse table in {chapter_title}: {e}")
            continue

        # Otherwise it's a paragraph or list item
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

    # Load existing data if available to preserve icons
    existing_data = {}
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            
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
            
        # Extract title from the first heading line
        # New KPBR format: "# CHAPTER I — DEFINITIONS"
        # KMBR format:     "# Chapter 1: Definitions"
        title_match = re.search(r'^#\s+(.*)', content)
        full_title = title_match.group(1).strip() if title_match else md_file.stem
        if ' — ' in full_title:
            # "CHAPTER I — DEFINITIONS" → "DEFINITIONS"
            chapter_title = full_title.split(' — ', 1)[1].strip()
        elif re.match(r'^Chapter\s+\d+:\s+', full_title, re.I):
            # "Chapter 1: Definitions" → "Definitions"
            chapter_title = re.sub(r'^Chapter\s+\d+:\s+', '', full_title, flags=re.I).strip()
        else:
            chapter_title = full_title
        
        # Clean up known artifacts
        content = re.sub(r'This is a digitally signed Gazette\.', '', content, flags=re.I)
        content = re.sub(r'Authenticity may be verified through https://compose\.kerala\.gov\.in/ \d+', '', content, flags=re.I)
        content = re.sub(r'KERALA MUNICIPALITY BUILDING RULES.*', '', content, flags=re.I)

        parsed_chapter = parse_markdown_to_json(content, chapter_title)
        new_content[chapter_id] = parsed_chapter
        
        # Preserve or update icon
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
