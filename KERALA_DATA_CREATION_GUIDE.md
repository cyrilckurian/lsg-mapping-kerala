# Kerala District Officials Data Creation Guide

This guide explains how to create district-level data for Kerala similar to the BLR City Officials map.

## Overview

The BLR City Officials map uses:
- **GeoJSON** files for geographic boundaries
- **JSON/CSV** files for officials information
- **Scripts** to process and merge data

For Kerala, we'll create:
1. District boundary GeoJSON files (14 districts)
2. LSG boundary GeoJSON files (1200+ local bodies)
3. Officials database (JSON/CSV format)
4. Processing scripts to merge everything

---

## Data Sources

### 1. Geographic Boundaries (Already Available!)

**OpenDataKerala LSG Data Repository:**
- URL: `https://github.com/opendatakerala/lsg-kerala-data`
- Contains: All 1200+ LSG boundaries in GeoJSON, KML, and Shapefile formats
- Includes:
  - 941 Grama Panchayats
  - 152 Block Panchayats
  - 14 District Panchayats
  - 87 Municipalities
  - 6 Municipal Corporations

**Direct Download:**
```bash
# Download the latest release
wget https://github.com/opendatakerala/lsg-kerala-data/releases/download/v1.0/kerala_lsg_data.geojson

# Or clone the entire repository
git clone https://github.com/opendatakerala/lsg-kerala-data.git
```

### 2. Officials Data (Needs to be Collected)

You'll need to gather:
- LSG head names (President/Mayor/Chairperson)
- LSG Secretary/Commissioner names
- Contact information (phone, email)
- Office addresses
- District Collector information
- MLA and MP information

**Data Sources:**
- `lsgkerala.gov.in` - Official LSG Kerala website
- Individual LSG websites
- Kerala Government directories
- Electoral Commission data
- Wikipedia/Wikidata

---

## Step-by-Step Data Creation Process

### Step 1: Download Geographic Data

```bash
# Create project structure
mkdir kerala-officials-map
cd kerala-officials-map
mkdir -p data/raw data/processed scripts

# Download LSG boundaries
cd data/raw
wget https://github.com/opendatakerala/lsg-kerala-data/releases/download/v1.0/kerala_lsg_data.geojson

# Or use curl
curl -L -o kerala_lsg_data.geojson \
  https://github.com/opendatakerala/lsg-kerala-data/releases/download/v1.0/kerala_lsg_data.geojson
```

### Step 2: Examine the GeoJSON Structure

The downloaded GeoJSON has this structure:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Thiruvananthapuram Corporation",
        "name:ml": "തിരുവനന്തപുരം കോർപ്പറേഷൻ",
        "admin_level": "8",
        "boundary": "administrative",
        "type": "boundary",
        "wikidata": "Q2095612",
        "wikipedia": "en:Thiruvananthapuram"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon, lat], [lon, lat], ...]]
      }
    }
  ]
}
```

### Step 3: Create Officials Database Template

Create a CSV file structure for officials data.

**File: `data/raw/lsg_officials_template.csv`**

```csv
lsg_id,lsg_name,lsg_name_ml,lsg_type,district,president_name,president_contact,president_email,secretary_name,secretary_contact,secretary_email,office_address,website,wikidata_id,mla_constituency,mp_constituency
KL-TVM-001,Thiruvananthapuram Corporation,തിരുവനന്തപുരം കോർപ്പറേഷൻ,corporation,Thiruvananthapuram,,,,,,,,,Q2095612,,
```

### Step 4: Process and Merge Data

See the Python scripts section below for processing scripts.

---

## Python Scripts for Data Processing

### Script 1: Extract District Boundaries

**File: `scripts/01_extract_districts.py`**

```python
#!/usr/bin/env python3
"""
Extract district-level boundaries from LSG data
"""

import json
import geopandas as gpd
from shapely.ops import unary_union

def extract_districts(input_geojson, output_geojson):
    """Extract and dissolve LSG boundaries by district"""
    
    # Read the LSG GeoJSON
    gdf = gpd.read_file(input_geojson)
    
    # Extract district from name or properties
    # This needs to be customized based on actual data structure
    # You may need to add a district field manually
    
    print(f"Loaded {len(gdf)} LSG features")
    print("Columns:", gdf.columns.tolist())
    print("\nSample properties:")
    print(gdf.head())
    
    # Group by district and dissolve
    if 'district' in gdf.columns:
        districts_gdf = gdf.dissolve(by='district', as_index=False)
        
        # Save to new GeoJSON
        districts_gdf.to_file(output_geojson, driver='GeoJSON')
        print(f"\nExtracted {len(districts_gdf)} districts")
        print(f"Saved to: {output_geojson}")
    else:
        print("\nNo 'district' field found. You'll need to add district mapping.")
        print("Create a CSV mapping LSG names to districts first.")

if __name__ == "__main__":
    extract_districts(
        "data/raw/kerala_lsg_data.geojson",
        "data/processed/kerala_districts.geojson"
    )
```

### Script 2: Add District Field to LSG Data

**File: `scripts/02_add_district_field.py`**

```python
#!/usr/bin/env python3
"""
Add district field to LSG GeoJSON based on mapping
"""

import json
import pandas as pd

# Kerala districts and their LSGs mapping
# This is a simplified version - you'll need to complete this
DISTRICT_MAPPING = {
    "Thiruvananthapuram": [
        "Thiruvananthapuram Corporation",
        "Neyyattinkara Municipality",
        # ... add all LSGs
    ],
    "Kollam": [
        "Kollam Corporation",
        # ... add all LSGs
    ],
    # ... add all 14 districts
}

def add_district_field(input_geojson, output_geojson, mapping):
    """Add district field to each LSG feature"""
    
    with open(input_geojson, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create reverse mapping: lsg_name -> district
    lsg_to_district = {}
    for district, lsgs in mapping.items():
        for lsg in lsgs:
            lsg_to_district[lsg] = district
    
    # Add district field to each feature
    matched = 0
    unmatched = []
    
    for feature in data['features']:
        lsg_name = feature['properties'].get('name', '')
        
        if lsg_name in lsg_to_district:
            feature['properties']['district'] = lsg_to_district[lsg_name]
            matched += 1
        else:
            unmatched.append(lsg_name)
            feature['properties']['district'] = 'Unknown'
    
    # Save updated GeoJSON
    with open(output_geojson, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Matched: {matched} LSGs")
    print(f"Unmatched: {len(unmatched)} LSGs")
    
    if unmatched:
        print("\nUnmatched LSGs:")
        for lsg in unmatched[:10]:  # Show first 10
            print(f"  - {lsg}")

if __name__ == "__main__":
    add_district_field(
        "data/raw/kerala_lsg_data.geojson",
        "data/processed/kerala_lsg_with_districts.geojson",
        DISTRICT_MAPPING
    )
```

### Script 3: Simplify GeoJSON for Web

**File: `scripts/03_simplify_geojson.py`**

```python
#!/usr/bin/env python3
"""
Simplify GeoJSON files for better web performance
"""

import geopandas as gpd

def simplify_geojson(input_file, output_file, tolerance=0.001):
    """
    Simplify geometry to reduce file size
    
    tolerance: smaller = more detailed, larger = more simplified
    0.001 degrees ≈ 111 meters at equator
    """
    
    print(f"Reading {input_file}...")
    gdf = gpd.read_file(input_file)
    
    original_size = len(str(gdf.to_json()))
    print(f"Original size: {original_size:,} bytes")
    
    # Simplify geometry
    print(f"Simplifying with tolerance={tolerance}...")
    gdf['geometry'] = gdf['geometry'].simplify(tolerance, preserve_topology=True)
    
    # Save simplified version
    gdf.to_file(output_file, driver='GeoJSON')
    
    simplified_size = len(str(gdf.to_json()))
    print(f"Simplified size: {simplified_size:,} bytes")
    print(f"Reduction: {100 * (1 - simplified_size/original_size):.1f}%")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    # Simplify LSG boundaries
    simplify_geojson(
        "data/processed/kerala_lsg_with_districts.geojson",
        "data/processed/kerala_lsg_simplified.geojson",
        tolerance=0.001  # Adjust based on needs
    )
    
    # Simplify district boundaries
    simplify_geojson(
        "data/processed/kerala_districts.geojson",
        "data/processed/kerala_districts_simplified.geojson",
        tolerance=0.005  # Districts can be more simplified
    )
```

### Script 4: Merge Officials Data

**File: `scripts/04_merge_officials_data.py`**

```python
#!/usr/bin/env python3
"""
Merge officials data with GeoJSON
"""

import json
import pandas as pd

def merge_officials_data(geojson_file, officials_csv, output_file):
    """Merge officials information into GeoJSON properties"""
    
    # Read GeoJSON
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geo_data = json.load(f)
    
    # Read officials CSV
    officials_df = pd.read_csv(officials_csv)
    
    # Create lookup dictionary
    officials_dict = officials_df.set_index('lsg_name').to_dict('index')
    
    # Merge data
    matched = 0
    for feature in geo_data['features']:
        lsg_name = feature['properties'].get('name', '')
        
        if lsg_name in officials_dict:
            # Add all official fields to properties
            officials_info = officials_dict[lsg_name]
            feature['properties'].update({
                'officials': {
                    'president': {
                        'name': officials_info.get('president_name', ''),
                        'contact': officials_info.get('president_contact', ''),
                        'email': officials_info.get('president_email', '')
                    },
                    'secretary': {
                        'name': officials_info.get('secretary_name', ''),
                        'contact': officials_info.get('secretary_contact', ''),
                        'email': officials_info.get('secretary_email', '')
                    }
                },
                'office_address': officials_info.get('office_address', ''),
                'website': officials_info.get('website', ''),
                'mla_constituency': officials_info.get('mla_constituency', ''),
                'mp_constituency': officials_info.get('mp_constituency', '')
            })
            matched += 1
    
    # Save merged GeoJSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geo_data, f, ensure_ascii=False, indent=2)
    
    print(f"Merged officials data for {matched} LSGs")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    merge_officials_data(
        "data/processed/kerala_lsg_simplified.geojson",
        "data/raw/lsg_officials.csv",
        "data/processed/kerala_lsg_final.geojson"
    )
```

### Script 5: Generate Search Index

**File: `scripts/05_generate_search_index.py`**

```python
#!/usr/bin/env python3
"""
Generate search index for fast client-side search
"""

import json

def generate_search_index(geojson_file, output_file):
    """Create a lightweight search index"""
    
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    search_index = []
    
    for feature in data['features']:
        props = feature['properties']
        
        # Calculate centroid for map centering
        if feature['geometry']['type'] == 'Polygon':
            coords = feature['geometry']['coordinates'][0]
        elif feature['geometry']['type'] == 'MultiPolygon':
            coords = feature['geometry']['coordinates'][0][0]
        else:
            continue
        
        # Simple centroid calculation
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        centroid = [sum(lons)/len(lons), sum(lats)/len(lats)]
        
        search_entry = {
            'id': props.get('wikidata', ''),
            'name': props.get('name', ''),
            'name_ml': props.get('name:ml', ''),
            'type': props.get('lsg_type', 'lsg'),
            'district': props.get('district', ''),
            'centroid': centroid,
            'officials': props.get('officials', {})
        }
        
        search_index.append(search_entry)
    
    # Save search index
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    
    print(f"Generated search index with {len(search_index)} entries")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    generate_search_index(
        "data/processed/kerala_lsg_final.geojson",
        "data/processed/search_index.json"
    )
```

---

## Installation & Setup

### 1. Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install geopandas pandas shapely fiona pyproj
```

### 2. Run the Processing Pipeline

```bash
# Make scripts executable
chmod +x scripts/*.py

# Run in order
python scripts/01_extract_districts.py
python scripts/02_add_district_field.py
python scripts/03_simplify_geojson.py
python scripts/04_merge_officials_data.py
python scripts/05_generate_search_index.py
```

---

## Data Collection Strategy for Officials

### Option 1: Manual Data Entry

Create a Google Sheet or Excel file with the template structure and fill it manually by:
1. Visiting individual LSG websites
2. Contacting LSG offices directly
3. Using government directories

### Option 2: Web Scraping

Create scrapers for:
- `lsgkerala.gov.in` - Main directory
- Individual LSG websites
- Government press releases

**Sample scraper structure:**

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_lsg_directory():
    """Scrape LSG Kerala website for officials data"""
    url = "https://lsgkerala.gov.in/en/lsgd-directory"
    # ... scraping logic
    pass
```

### Option 3: Crowdsourcing

1. Set up a GitHub repository
2. Create contribution guidelines
3. Use issues to track missing data
4. Accept pull requests with verified data

---

## File Structure Reference

Your final project structure should look like:

```
kerala-officials-map/
├── data/
│   ├── raw/
│   │   ├── kerala_lsg_data.geojson          # Downloaded from OpenDataKerala
│   │   ├── lsg_officials.csv                 # Officials data (to be created)
│   │   └── district_mapping.json             # LSG to district mapping
│   └── processed/
│       ├── kerala_districts.geojson          # District boundaries
│       ├── kerala_districts_simplified.geojson
│       ├── kerala_lsg_with_districts.geojson # LSGs with district field
│       ├── kerala_lsg_simplified.geojson     # Simplified for web
│       ├── kerala_lsg_final.geojson          # With officials data
│       └── search_index.json                 # Search index
├── scripts/
│   ├── 01_extract_districts.py
│   ├── 02_add_district_field.py
│   ├── 03_simplify_geojson.py
│   ├── 04_merge_officials_data.py
│   └── 05_generate_search_index.py
├── requirements.txt
└── README.md
```

---

## Next Steps

1. **Download the geographic data** from OpenDataKerala
2. **Create the district mapping** (LSG to district)
3. **Collect officials data** using one of the strategies above
4. **Run the processing scripts** to generate final files
5. **Integrate with web application** (Svelte/React/etc.)

---

## Additional Resources

- OpenDataKerala LSG Data: https://github.com/opendatakerala/lsg-kerala-data
- Map Kerala Portal: https://map.opendatakerala.org/
- LSG Kerala Official: https://lsgkerala.gov.in/
- OSM Wiki for Kerala: https://wiki.openstreetmap.org/wiki/Local_Bodies_in_Kerala
- GeoJSON Specification: https://geojson.org/

---

## Tips for Success

1. **Start Small**: Begin with one district (e.g., Thiruvananthapuram) and test the entire pipeline
2. **Verify Data**: Cross-check officials data with multiple sources
3. **Keep Data Current**: Set up a process to update officials data regularly
4. **Document Sources**: Keep track of where each piece of data came from
5. **Version Control**: Use Git to track changes in data files
6. **Community Engagement**: Work with OpenDataKerala community for help

---

## Troubleshooting

### Issue: GeoJSON too large for web
**Solution**: Increase simplification tolerance or use vector tiles (Mapbox)

### Issue: Missing district information
**Solution**: Manually create a mapping CSV with LSG names and districts

### Issue: Officials data quickly becomes outdated
**Solution**: Set up a quarterly update schedule and crowdsource updates

### Issue: Different name spellings
**Solution**: Create a name normalization function to handle variations

---

## License

Follow the same license as OpenDataKerala data:
- Data: Open Database License (ODbL)
- Code: MIT or GPL-3.0 (like BLR City Officials)
