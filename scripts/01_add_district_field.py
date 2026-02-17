#!/usr/bin/env python3
"""
Script 1: Add district field to LSG GeoJSON
Matches LSG names to districts using the district mapping
"""

import json
import sys
from pathlib import Path

# Import district mapping
from kerala_district_mapping import get_lsg_to_district_mapping


def normalize_name(name):
    """Normalize LSG names for better matching and display"""
    if not name:
        return ""

    # Convert to lowercase and strip whitespace
    normalized = name.lower().strip()

    # Aggressive suffix removal (order matters - longer first)
    suffixes = [
        ' municipal corporation',
        ' grama panchayath',
        ' grama panchayat',
        ' gramapanchayath',
        ' gramapanchayat',
        ' block panchayat',
        ' district panchayat',
        ' corporation',
        ' municipality',
        ' panchayath',
        ' panchayat'
    ]

    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)].strip()
            # Loop again in case there are multiple suffixes (e.g. "Name Grama Panchayat Panchayat")
            return normalize_name(normalized)

    return normalized.title()

def add_district_field(input_file, output_file):
    """Add district field to each LSG feature in GeoJSON"""

    print(f"Reading {input_file}...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        print("Please run setup.sh first to download the data")
        sys.exit(1)

    # Get district mapping
    lsg_to_district = get_lsg_to_district_mapping()

    # Also create normalized mapping for fuzzy matching
    normalized_mapping = {}
    for lsg, district in lsg_to_district.items():
        normalized_mapping[normalize_name(lsg)] = district

    # Process each feature
    matched = 0
    unmatched = []
    features_by_type = {'corporation': 0, 'municipality': 0, 'panchayat': 0, 'unknown': 0}

    print(f"\nProcessing {len(data['features'])} features...")

    for feature in data['features']:
        props = feature['properties']
        lsg_name = props.get('name', '')
        raw_district = props.get('District', '')

        district = None

        # 1. Try using the raw District field if it exists and is not "Unknown"
        if raw_district and raw_district != 'Unknown':
            district = raw_district
        
        # 2. Try exact match from mapping if raw district is missing
        if not district:
            district = lsg_to_district.get(lsg_name)

        # 3. Try normalized match if still no district
        if not district:
            normalized = normalize_name(lsg_name)
            district = normalized_mapping.get(normalized)

        # 4. Try matching with different suffixes
        if not district:
            for suffix in ['Corporation', 'Municipality', 'Grama Panchayat', 'Block Panchayat']:
                test_name = f"{lsg_name} {suffix}"
                district = lsg_to_district.get(test_name)
                if district:
                    break

        # Clean and update the name in properties
        props['name'] = normalize_name(lsg_name)

        # Add district to properties
        if district:
            props['district'] = district
            matched += 1
        else:
            props['district'] = 'Unknown'
            unmatched.append(lsg_name)

        # Infer LSG type from local_auth, name or admin_leve
        local_auth = props.get('local_auth', '').lower()
        admin_level = props.get('admin_leve', '')
        lsg_name_lower = lsg_name.lower()

        if local_auth == 'municipal_corporation' or 'corporation' in lsg_name_lower:
            lsg_type = 'municipal corporation'
        elif local_auth == 'municipality' or 'municipality' in lsg_name_lower:
            lsg_type = 'municipality'
        elif local_auth == 'gram_panchayat' or 'panchayat' in lsg_name_lower or 'panchayath' in lsg_name_lower:
            lsg_type = 'gram panchayat'
        elif admin_level == '4': # Usually higher level - likely municipality/corporation if not matched above
            lsg_type = 'municipality'
        elif admin_level == '8': # Usually gram panchayat
            lsg_type = 'gram panchayat'
        else:
            lsg_type = 'unknown'

        props['lsg_type'] = lsg_type
        features_by_type[lsg_type] = features_by_type.get(lsg_type, 0) + 1

    # Save updated GeoJSON
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total features: {len(data['features'])}")
    print(f"Matched to districts: {matched} ({100*matched/len(data['features']):.1f}%)")
    print(f"Unmatched: {len(unmatched)}")

    print("\nFeatures by type:")
    for lsg_type, count in sorted(features_by_type.items()):
        print(f"  {lsg_type.capitalize()}: {count}")

    if unmatched:
        print("\nFirst 20 unmatched LSGs:")
        for lsg in unmatched[:20]:
            print(f"  - {lsg}")

        if len(unmatched) > 20:
            print(f"  ... and {len(unmatched) - 20} more")

        print("\nNote: These LSGs need to be added to kerala_district_mapping.py")
        print("Most unmatched are likely Grama Panchayats (941 total)")

    print("\n✓ Successfully processed data")
    print(f"✓ Output saved to: {output_file}")

    return matched, len(unmatched)

def main():
    """Main function"""

    # File paths
    input_file = Path("data/raw/kerala_lsg_data.geojson")
    output_file = Path("data/processed/kerala_lsg_with_districts.geojson")

    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Process data
    add_district_field(input_file, output_file)

if __name__ == "__main__":
    main()
