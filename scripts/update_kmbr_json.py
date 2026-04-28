import os
import json
import re
from pathlib import Path

def parse_markdown_to_json(md_content, chapter_title):
    sections = []
    current_section = None
    
    lines = md_content.split('\n')
    
    # Pattern for section headers: ### 1. Title.-
    section_pattern = re.compile(r'^###\s+(\d+[A-Z]?)\.\s+(.*)')
    
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
            
            if len(table_lines) >= 3: # Header, separator, at least one row
                # Parse markdown table
                # Row 0: Headers
                # Row 1: Separator (---)
                # Row 2+: Data
                
                headers = [c.strip() for c in table_lines[0].split('|') if c.strip()]
                # Skip separator
                rows = []
                for row_line in table_lines[2:]:
                    row_data = [c.strip() for c in row_line.split('|')]
                    # Filter out empty ends
                    if row_line.startswith('|'): row_data = row_data[1:]
                    if row_line.endswith('|'): row_data = row_data[:-1]
                    rows.append([c.strip() for c in row_data])
                
                # Try to find table title in previous paragraph
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
            continue

        # Otherwise it's a paragraph or list item
        current_section["paragraphs"].append(line)
        i += 1
                
    return {
        "title": chapter_title,
        "sections": sections
    }

def main():
    kmbr_dir = Path("/Users/cyrilckurian/Desktop/Kerala-map/data/building_rules/kmbr")
    json_path = Path("/Users/cyrilckurian/Desktop/Kerala-map/web-app/src/lib/data/kmbr.json")
    
    if not json_path.exists():
        print(f"Error: {json_path} not found")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        kmbr_data = json.load(f)
        
    md_files = sorted(list(kmbr_dir.glob("chapter_*.md")))
    
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
            
        title_match = re.search(r'^# Chapter \d+:\s*(.*)', content)
        chapter_title = title_match.group(1).strip() if title_match else md_file.stem
        
        parsed_chapter = parse_markdown_to_json(content, chapter_title)
        new_content[chapter_id] = parsed_chapter
        
        # Preserve or update icon
        existing_chapter = next((c for c in kmbr_data.get("chapters", []) if c["id"] == chapter_id), None)
        icon = existing_chapter["icon"] if existing_chapter and "icon" in existing_chapter else "description"
        
        new_chapters.append({
            "id": chapter_id,
            "number": chapter_num,
            "title": chapter_title,
            "icon": icon
        })
        
    kmbr_data["chapters"] = new_chapters
    kmbr_data["content"] = new_content
    kmbr_data["lastUpdated"] = "Apr 2026"
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(kmbr_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully updated {json_path} with {len(new_chapters)} chapters.")

if __name__ == "__main__":
    main()
