#!/usr/bin/env python3
"""
Script 2: Extract district-level boundaries from LSG data
Creates a separate GeoJSON with just district boundaries
"""

import sys
from pathlib import Path

try:
    import geopandas as gpd
    from shapely.ops import unary_union
except ImportError:
    print("Error: geopandas is not installed")
    print("Please run: pip install geopandas")
    sys.exit(1)

def extract_districts(input_file, output_file):
    """Extract and dissolve LSG boundaries by district"""
    
    print(f"Reading {input_file}...")
    
    try:
        gdf = gpd.read_file(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    print(f"Loaded {len(gdf)} LSG features")
    
    # Check if district field exists
    if 'district' not in gdf.columns:
        print("\nError: 'district' field not found in data")
        print("Please run scripts/01_add_district_field.py first")
        sys.exit(1)
    
    # Remove features with unknown district
    unknown_count = len(gdf[gdf['district'] == 'Unknown'])
    if unknown_count > 0:
        print(f"\nWarning: {unknown_count} features have district='Unknown'")
        print("These will be excluded from district boundaries")
        gdf = gdf[gdf['district'] != 'Unknown']
    
    print(f"\nDistricts found:")
    districts = gdf['district'].unique()
    for i, district in enumerate(sorted(districts), 1):
        count = len(gdf[gdf['district'] == district])
        print(f"  {i}. {district}: {count} LSGs")
    
    # Dissolve by district
    print(f"\nDissolving {len(gdf)} LSGs into {len(districts)} districts...")
    districts_gdf = gdf.dissolve(
        by='district',
        as_index=False,
        aggfunc='first'  # Use first for simplicity as we only need district and geometry
    )
    
    # Keep only essential fields
    districts_gdf = districts_gdf[['district', 'geometry']]
    
    # Rename district column to name for consistency
    districts_gdf['name'] = districts_gdf['district']
    
    # Calculate area in square kilometers
    # Reproject to a metric CRS for accurate area calculation
    districts_gdf_metric = districts_gdf.to_crs('EPSG:32643')  # WGS 84 / UTM zone 43N (Kerala)
    districts_gdf['area_sq_km'] = districts_gdf_metric.geometry.area / 1_000_000
    
    # Sort by name
    districts_gdf = districts_gdf.sort_values('name')
    
    # Save to GeoJSON
    print(f"\nSaving to {output_file}...")
    districts_gdf.to_file(output_file, driver='GeoJSON')
    
    # Print summary
    print("\n" + "="*60)
    print("DISTRICT BOUNDARIES EXTRACTED")
    print("="*60)
    print(f"Total districts: {len(districts_gdf)}")
    print(f"\nDistricts with areas:")
    
    for _, row in districts_gdf.iterrows():
        print(f"  {row['name']:25s} {row['area_sq_km']:10,.2f} sq km")
    
    total_area = districts_gdf['area_sq_km'].sum()
    print(f"\nTotal area: {total_area:,.2f} sq km")
    print(f"(Kerala actual area: ~38,852 sq km)")
    
    print(f"\n✓ District boundaries saved to: {output_file}")

def main():
    """Main function"""
    
    # File paths
    input_file = Path("data/processed/kerala_lsg_with_districts.geojson")
    output_file = Path("data/processed/kerala_districts.geojson")
    
    # Check if input exists
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        print("Please run scripts/01_add_district_field.py first")
        sys.exit(1)
    
    # Create output directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract districts
    extract_districts(input_file, output_file)

if __name__ == "__main__":
    main()
