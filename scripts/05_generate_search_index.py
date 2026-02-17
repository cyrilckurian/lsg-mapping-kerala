#!/usr/bin/env python3
"""
Script 5: Generate search index for fast client-side search
Creates a lightweight JSON file for searching LSGs
"""

import json
import sys
from pathlib import Path


def calculate_centroid(geometry):
    """Calculate simple centroid for a geometry"""

    geom_type = geometry.get('type')
    coords = geometry.get('coordinates', [])

    if not coords:
        return None

    try:
        if geom_type == 'Polygon':
            # Get exterior ring
            ring = coords[0] if coords else []
        elif geom_type == 'MultiPolygon':
            # Get first polygon's exterior ring
            ring = coords[0][0] if coords and coords[0] else []
        else:
            return None

        if not ring:
            return None

        # Calculate average lon/lat
        lons = [point[0] for point in ring]
        lats = [point[1] for point in ring]

        if lons and lats:
            return [sum(lons) / len(lons), sum(lats) / len(lats)]

    except (IndexError, TypeError):
        return None

    return None

def generate_search_index(geojson_file, output_file):
    """Create a lightweight search index"""

    print(f"Reading {geojson_file}...")

    if not geojson_file.exists():
        print(f"Error: File not found: {geojson_file}")
        return False

    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Processing {len(data['features'])} features...")

    search_index = []
    skipped = 0

    for i, feature in enumerate(data['features'], 1):
        props = feature['properties']

        # Calculate centroid
        centroid = calculate_centroid(feature.get('geometry', {}))

        if not centroid:
            skipped += 1
            continue

        # Create search entry with essential information
        search_entry = {
            'id': i,
            'name': props.get('name', ''),
            'name_ml': props.get('name:ml', ''),
            'type': props.get('lsg_type', 'lsg'),
            'district': props.get('district', ''),
            'centroid': centroid,
        }

        # Add officials if available
        if 'officials' in props:
            officials = props['officials']

            # Extract president/mayor info
            president = officials.get('president', {})
            if president.get('name'):
                search_entry['head'] = {
                    'name': president.get('name', ''),
                    'title': 'Mayor' if search_entry['type'] == 'corporation' else 'President'
                }

            # Extract secretary info
            secretary = officials.get('secretary', {})
            if secretary.get('name'):
                search_entry['secretary'] = secretary.get('name', '')

        # Add contact info if available
        if props.get('website'):
            search_entry['website'] = props['website']

        if props.get('wikidata'):
            search_entry['wikidata'] = props['wikidata']

        # Add constituency info
        if props.get('mla_constituency'):
            search_entry['mla_constituency'] = props['mla_constituency']

        if props.get('mp_constituency'):
            search_entry['mp_constituency'] = props['mp_constituency']

        search_index.append(search_entry)

    # Save search index
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)

    # Calculate file sizes
    input_size = geojson_file.stat().st_size / 1024
    output_size = output_file.stat().st_size / 1024

    # Print summary
    print("\n" + "="*60)
    print("SEARCH INDEX GENERATED")
    print("="*60)
    print(f"Total entries: {len(search_index)}")
    print(f"Skipped (no geometry): {skipped}")

    # Count by type
    type_counts = {}
    district_counts = {}

    for entry in search_index:
        lsg_type = entry.get('type', 'unknown')
        district = entry.get('district', 'Unknown')

        type_counts[lsg_type] = type_counts.get(lsg_type, 0) + 1
        district_counts[district] = district_counts.get(district, 0) + 1

    print("\nEntries by type:")
    for lsg_type, count in sorted(type_counts.items()):
        print(f"  {lsg_type.capitalize()}: {count}")

    print("\nEntries by district:")
    for district, count in sorted(district_counts.items()):
        print(f"  {district}: {count}")

    print("\nFile sizes:")
    print(f"  Original GeoJSON: {input_size:,.2f} KB")
    print(f"  Search index: {output_size:,.2f} KB")
    print(f"  Reduction: {100 * (1 - output_size/input_size):.1f}%")

    print(f"\n✓ Search index saved to: {output_file}")

    # Generate usage example
    usage_example = f"""

Usage Example (JavaScript):

// Load search index
const searchIndex = await fetch('{output_file.name}').then(r => r.json());

// Search by name
function searchByName(query) {{
  const q = query.toLowerCase();
  return searchIndex.filter(lsg =>
    lsg.name.toLowerCase().includes(q) ||
    (lsg.name_ml && lsg.name_ml.includes(q))
  );
}}

// Filter by district
function getByDistrict(district) {{
  return searchIndex.filter(lsg => lsg.district === district);
}}

// Get all corporations
const corporations = searchIndex.filter(lsg => lsg.type === 'corporation');
"""

    print(usage_example)

    return True

def main():
    """Main function"""

    # File paths
    geojson_file = Path("data/processed/kerala_lsg_final.geojson")
    output_file = Path("data/processed/search_index.json")

    # Generate search index
    success = generate_search_index(geojson_file, output_file)

    if not success:
        print("\nError: Could not generate search index")
        print("Make sure you've run all previous scripts")
        sys.exit(1)

if __name__ == "__main__":
    main()
