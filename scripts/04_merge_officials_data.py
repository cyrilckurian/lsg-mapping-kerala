#!/usr/bin/env python3
"""
Script 4: Merge officials data with GeoJSON
Adds officials information from CSV to the GeoJSON properties
"""

import json
import sys
from pathlib import Path

import csv
import shutil

def normalize_name(name):
    """Normalize LSG names for better matching"""
    if not name:
        return ""
    normalized = name.lower().strip()
    suffixes = [
        ' municipal corporation', ' corporation', ' municipality',
        ' grama panchayat', ' grama panchayath', ' gramapanchayat', ' gramapanchayath',
        ' block panchayat', ' district panchayat', ' panchayath', ' panchayat'
    ]
    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)].strip()
            break
    return normalized

def merge_officials_data(geojson_file, officials_csv, output_file):
    """Merge officials information into GeoJSON properties"""

    print(f"Reading GeoJSON: {geojson_file}...")

    # Check if files exist
    if not geojson_file.exists():
        print(f"Error: GeoJSON file not found: {geojson_file}")
        return False

    if not officials_csv.exists():
        print(f"Error: Officials CSV file not found: {officials_csv}")
        print("\nPlease create this file with officials data.")
        print("You can start with the template at: data/raw/lsg_officials_template.csv")
        return False

    # Read GeoJSON
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geo_data = json.load(f)

    print(f"  Features: {len(geo_data['features'])}")

    # Read officials CSV using standard csv module
    print(f"\nReading officials data: {officials_csv}...")
    try:
        with open(officials_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            officials_records = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False

    print(f"  Records: {len(officials_records)}")

    # Create lookup dictionary by normalized LSG name
    officials_dict = {}
    for row in officials_records:
        lsg_name = row.get('lsg_name', '')
        if lsg_name:
            officials_dict[normalize_name(lsg_name)] = row

    print(f"  Unique LSGs in CSV: {len(officials_dict)}")

    # Merge data
    print("\nMerging data...")
    matched = 0
    updated = 0

    for feature in geo_data['features']:
        props = feature['properties']
        lsg_name = props.get('name', '')
        norm_name = normalize_name(lsg_name)

        if norm_name in officials_dict:
            matched += 1
            officials_info = officials_dict[norm_name]

            # Check if there's actual data (not just empty fields)
            has_data = any([
                officials_info.get('president_name'),
                officials_info.get('secretary_name'),
                officials_info.get('office_address'),
                officials_info.get('website')
            ])

            if has_data:
                updated += 1

            # Add officials structure
            props['officials'] = {
                'president': {
                    'name': officials_info.get('president_name', ''),
                    'party': officials_info.get('president_party', ''),
                    'contact': officials_info.get('president_contact', ''),
                    'email': officials_info.get('president_email', '')
                },
                'secretary': {
                    'name': officials_info.get('secretary_name', ''),
                    'contact': officials_info.get('secretary_contact', ''),
                    'email': officials_info.get('secretary_email', '')
                }
            }

            # Add other fields
            if officials_info.get('office_address'):
                props['office_address'] = officials_info['office_address']

            if officials_info.get('website'):
                props['website'] = officials_info['website']

            if officials_info.get('mla_constituency'):
                props['mla_constituency'] = officials_info['mla_constituency']

            if officials_info.get('mp_constituency'):
                props['mp_constituency'] = officials_info['mp_constituency']

            if officials_info.get('notes'):
                props['notes'] = officials_info['notes']

    # Save merged GeoJSON
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geo_data, f, ensure_ascii=False, indent=2)

    # Print summary
    print("\n" + "="*60)
    print("OFFICIALS DATA MERGE COMPLETE")
    print("="*60)
    print(f"Total LSGs in GeoJSON: {len(geo_data['features'])}")
    print(f"Officials records in CSV: {len(officials_dict)}")
    print(f"Matched LSGs: {matched}")
    print(f"LSGs with actual data: {updated}")
    print(f"Coverage: {100*updated/len(geo_data['features']):.1f}%")

    if matched < len(geo_data['features']):
        unmatched = len(geo_data['features']) - matched
        print(f"\nNote: {unmatched} LSGs don't have officials data yet")
        print("Continue collecting data to improve coverage")

    print(f"\n✓ Merged data saved to: {output_file}")

    return True

def main():
    """Main function"""

    # File paths
    geojson_file = Path("data/processed/kerala_lsg_simplified.geojson")
    officials_csv = Path("data/raw/lsg_officials.csv")
    output_file = Path("data/processed/kerala_lsg_final.geojson")

    # Also accept template if actual file doesn't exist
    if not officials_csv.exists():
        template_file = Path("data/raw/lsg_officials_template.csv")
        if template_file.exists():
            print("Note: Using template file as starting point")
            print(f"Please rename and fill: {template_file} -> {officials_csv}")
            officials_csv = template_file

    # Prefer simplified version, fall back to unsimplified
    if not geojson_file.exists():
        fallback = Path("data/processed/kerala_lsg_with_districts.geojson")
        if fallback.exists():
            print(f"Note: {geojson_file} not found. Using fallback: {fallback}")
            geojson_file = fallback
        else:
            print(f"Error: Neither {geojson_file} nor {fallback} exist.")
            return False

    # Merge data
    success = merge_officials_data(geojson_file, officials_csv, output_file)

    if success:
        # Sync to web app static directory
        static_output = Path("web-app/static/data/kerala_lsg_final.geojson")
        try:
            import shutil
            static_output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output_file, static_output)
            print(f"✓ Synced to web app: {static_output}")
        except Exception as e:
            print(f"Warning: Could not sync to web app: {e}")
    else:
        print("\nTroubleshooting:")
        print("1. Make sure you've run the previous scripts")
        print("2. Create lsg_officials.csv from the template")
        print("3. Fill in at least some officials data")
        sys.exit(1)

if __name__ == "__main__":
    main()
