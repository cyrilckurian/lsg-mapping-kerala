# Data Directory

## Raw Data

### kerala_lsg_data.geojson
- Source: OpenDataKerala (https://github.com/opendatakerala/lsg-kerala-data)
- Contains: All 1200+ LSG boundaries in Kerala
- Format: GeoJSON
- License: Open Database License (ODbL)

### lsg_officials_template.csv
- Template for collecting officials data
- Fill this with actual data from LSG websites, directories, etc.

## Processed Data

Generated files will be saved here after running processing scripts:
- kerala_lsg_with_districts.geojson - LSGs with district field added
- kerala_districts.geojson - District-level boundaries
- kerala_lsg_simplified.geojson - Simplified for web use
- kerala_lsg_final.geojson - With officials data merged
- search_index.json - Fast client-side search

## Data Collection

To collect officials data:
1. Visit individual LSG websites
2. Check https://lsgkerala.gov.in/
3. Contact LSG offices directly
4. Use government directories
5. Verify with multiple sources
