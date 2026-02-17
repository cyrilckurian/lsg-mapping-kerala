#!/usr/bin/env python3
"""
Script 3: Simplify GeoJSON files for better web performance
Reduces file size while maintaining visual accuracy
"""

import sys
from pathlib import Path

try:
    import geopandas as gpd
except ImportError:
    print("Error: geopandas is not installed")
    print("Please run: pip install geopandas")
    sys.exit(1)

def get_file_size(filepath):
    """Get file size in KB"""
    return filepath.stat().st_size / 1024

def simplify_geojson(input_file, output_file, tolerance=0.001, preserve_topology=True):
    """
    Simplify geometry to reduce file size

    Args:
        input_file: Input GeoJSON file path
        output_file: Output GeoJSON file path
        tolerance: Simplification tolerance in degrees
                  0.001 degrees ≈ 111 meters at equator
                  0.0001 = very detailed (11m)
                  0.001 = detailed (111m)
                  0.005 = simplified (555m)
                  0.01 = very simplified (1.1km)
        preserve_topology: Ensure no invalid geometries are created
    """

    print(f"\nProcessing: {input_file.name}")
    print(f"Tolerance: {tolerance} degrees (~{int(tolerance * 111_000)}m)")
    print("-" * 60)

    # Check if input exists
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return False

    # Get original file size
    original_size = get_file_size(input_file)
    print(f"Original size: {original_size:,.2f} KB")

    # Read GeoJSON
    print("Reading GeoJSON...")
    gdf = gpd.read_file(input_file)

    original_coords = sum(len(geom.exterior.coords) if geom.geom_type == 'Polygon'
                         else sum(len(p.exterior.coords) for p in geom.geoms)
                         if geom.geom_type == 'MultiPolygon' else 0
                         for geom in gdf.geometry)

    print(f"Features: {len(gdf)}")
    print(f"Coordinate points: {original_coords:,}")

    # Simplify geometry
    print("Simplifying...")
    gdf['geometry'] = gdf['geometry'].simplify(
        tolerance=tolerance,
        preserve_topology=preserve_topology
    )

    # Check for invalid geometries
    invalid = ~gdf.is_valid
    if invalid.any():
        print(f"Warning: {invalid.sum()} invalid geometries after simplification")
        print("Attempting to fix...")
        gdf.loc[invalid, 'geometry'] = gdf.loc[invalid, 'geometry'].buffer(0)

    # Count new coordinates
    simplified_coords = sum(len(geom.exterior.coords) if geom.geom_type == 'Polygon'
                           else sum(len(p.exterior.coords) for p in geom.geoms)
                           if geom.geom_type == 'MultiPolygon' else 0
                           for geom in gdf.geometry)

    # Save simplified version
    print("Saving...")
    gdf.to_file(output_file, driver='GeoJSON')

    # Get new file size
    simplified_size = get_file_size(output_file)

    # Print results
    size_reduction = 100 * (1 - simplified_size / original_size)
    coord_reduction = 100 * (1 - simplified_coords / original_coords)

    print("\n✓ Simplified successfully")
    print(f"  New size: {simplified_size:,.2f} KB")
    print(f"  Size reduction: {size_reduction:.1f}%")
    print(f"  Coordinate points: {simplified_coords:,}")
    print(f"  Coordinate reduction: {coord_reduction:.1f}%")

    return True

def main():
    """Main function"""

    # File paths and tolerances
    files_to_simplify = [
        {
            'input': Path("data/processed/kerala_lsg_with_districts.geojson"),
            'output': Path("data/processed/kerala_lsg_simplified.geojson"),
            'tolerance': 0.001,  # ~111m - good for LSG boundaries
            'description': 'LSG boundaries'
        },
        {
            'input': Path("data/processed/kerala_districts.geojson"),
            'output': Path("data/processed/kerala_districts_simplified.geojson"),
            'tolerance': 0.005,  # ~555m - districts can be more simplified
            'description': 'District boundaries'
        }
    ]

    print("="*60)
    print("GEOJSON SIMPLIFICATION FOR WEB")
    print("="*60)

    success_count = 0

    for config in files_to_simplify:
        if config['input'].exists():
            if simplify_geojson(config['input'], config['output'], config['tolerance']):
                success_count += 1
        else:
            print(f"\nSkipping: {config['description']} (file not found)")
            print(f"  Expected: {config['input']}")

    # Summary
    print("\n" + "="*60)
    print(f"Successfully simplified {success_count}/{len(files_to_simplify)} files")
    print("="*60)

    if success_count < len(files_to_simplify):
        print("\nNote: Some files were skipped because they don't exist yet.")
        print("Make sure to run the previous scripts in order:")
        print("  1. scripts/01_add_district_field.py")
        print("  2. scripts/02_extract_districts.py")
        print("  3. scripts/03_simplify_geojson.py (this script)")

if __name__ == "__main__":
    main()
