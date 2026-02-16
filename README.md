# Kerala Officials Map - Data Pipeline

Complete data processing pipeline to create district and LSG data for Kerala, similar to the BLR City Officials map.

## 🚀 Quick Start

```bash
# 1. Clone/download this project
cd kerala-officials-data-pipeline

# 2. Run setup (downloads data, creates environment)
chmod +x setup.sh
./setup.sh

# 3. Activate Python environment
source venv/bin/activate

# 4. Run processing pipeline
python scripts/01_add_district_field.py
python scripts/02_extract_districts.py
python scripts/03_simplify_geojson.py

# 5. Add officials data (see below)
# Edit: data/raw/lsg_officials.csv

# 6. Merge officials data
python scripts/04_merge_officials_data.py
python scripts/05_generate_search_index.py
```

## 📁 Project Structure

```
kerala-officials-data-pipeline/
├── data/
│   ├── raw/                                  # Source data
│   │   ├── kerala_lsg_data.geojson          # Downloaded from OpenDataKerala
│   │   ├── lsg_officials_template.csv       # Template for officials data
│   │   └── lsg_officials.csv                # Your officials data (create this)
│   └── processed/                            # Generated files
│       ├── kerala_lsg_with_districts.geojson
│       ├── kerala_districts.geojson
│       ├── kerala_lsg_simplified.geojson
│       ├── kerala_lsg_final.geojson         # Final output
│       └── search_index.json                 # Search index
├── scripts/                                  # Processing scripts
│   ├── 01_add_district_field.py
│   ├── 02_extract_districts.py
│   ├── 03_simplify_geojson.py
│   ├── 04_merge_officials_data.py
│   └── 05_generate_search_index.py
├── kerala_district_mapping.py                # District to LSG mapping
├── requirements.txt                          # Python dependencies
├── setup.sh                                  # Setup script
└── README.md                                 # This file
```

## 📊 Data Sources

### Geographic Boundaries (Automated)
- **Source**: OpenDataKerala - https://github.com/opendatakerala/lsg-kerala-data
- **Contains**: All 1200+ LSG boundaries in Kerala
- **Format**: GeoJSON
- **License**: Open Database License (ODbL)
- **Downloaded by**: `setup.sh` script

### Officials Data (Manual Collection Required)
You need to collect:
- LSG President/Mayor/Chairperson names
- Secretary/Commissioner names
- Contact information (phone, email)
- Office addresses
- Websites
- MLA/MP constituency info

**Where to find this data:**
1. Individual LSG websites
2. https://lsgkerala.gov.in/
3. Government directories
4. Contact LSG offices directly
5. Wikipedia/Wikidata

## 📝 Creating Officials Data

### Option 1: Start with Template

```bash
# Copy template
cp data/raw/lsg_officials_template.csv data/raw/lsg_officials.csv

# Edit with your favorite editor or spreadsheet app
# Fill in the officials information
```

### Option 2: Use Google Sheets

1. Upload `data/raw/lsg_officials_template.csv` to Google Sheets
2. Share with team members for collaborative data entry
3. Download as CSV when done
4. Save as `data/raw/lsg_officials.csv`

### CSV Format

```csv
lsg_id,lsg_name,lsg_name_ml,lsg_type,district,president_name,president_contact,president_email,secretary_name,secretary_contact,secretary_email,office_address,website,wikidata_id,mla_constituency,mp_constituency
KL-TVM-001,Thiruvananthapuram Corporation,തിരുവനന്തപുരം കോർപ്പറേഷൻ,corporation,Thiruvananthapuram,Mayor Name,1234567890,mayor@tvm.gov.in,Commissioner Name,9876543210,commissioner@tvm.gov.in,Main Office Address,https://trivandrum.corporation.kerala.gov.in/,Q2095612,Thiruvananthapuram,Thiruvananthapuram
```

## 🔄 Processing Pipeline

### Script 1: Add District Field
```bash
python scripts/01_add_district_field.py
```
- Reads raw LSG GeoJSON
- Adds district field to each LSG
- Infers LSG type (corporation/municipality/panchayat)
- Output: `kerala_lsg_with_districts.geojson`

### Script 2: Extract Districts
```bash
python scripts/02_extract_districts.py
```
- Dissolves LSG boundaries by district
- Creates 14 district-level boundaries
- Calculates areas
- Output: `kerala_districts.geojson`

### Script 3: Simplify for Web
```bash
python scripts/03_simplify_geojson.py
```
- Reduces file size for web performance
- Maintains visual accuracy
- Typically reduces size by 70-90%
- Output: `kerala_lsg_simplified.geojson`, `kerala_districts_simplified.geojson`

### Script 4: Merge Officials Data
```bash
python scripts/04_merge_officials_data.py
```
- Merges officials info from CSV into GeoJSON
- Adds structured officials data to properties
- Output: `kerala_lsg_final.geojson`

### Script 5: Generate Search Index
```bash
python scripts/05_generate_search_index.py
```
- Creates lightweight search index
- Includes centroids for map centering
- Much smaller than full GeoJSON
- Output: `search_index.json`

## 📦 Output Files

### For Web Application

Use these files in your web app:

1. **kerala_lsg_final.geojson** (~2-5 MB)
   - Full LSG boundaries with all data
   - Use for map display

2. **kerala_districts_simplified.geojson** (~100-200 KB)
   - District boundaries
   - Use as base layer

3. **search_index.json** (~100-300 KB)
   - Fast client-side search
   - Load initially for search functionality

### Sample Integration (Mapbox GL JS)

```javascript
// Initialize map
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v10',
  center: [76.2711, 10.8505], // Kerala center
  zoom: 7
});

// Load district boundaries
map.on('load', async () => {
  // Add districts layer
  const districts = await fetch('kerala_districts_simplified.geojson')
    .then(r => r.json());
  
  map.addSource('districts', {
    type: 'geojson',
    data: districts
  });
  
  map.addLayer({
    id: 'districts-fill',
    type: 'fill',
    source: 'districts',
    paint: {
      'fill-color': '#088',
      'fill-opacity': 0.1
    }
  });
  
  // Load search index
  const searchIndex = await fetch('search_index.json')
    .then(r => r.json());
  
  // Implement search...
});
```

## 🌍 Kerala Statistics

- **Districts**: 14
- **Corporations**: 6
- **Municipalities**: 87
- **Block Panchayats**: 152
- **Grama Panchayats**: 941
- **Total LSGs**: 1,200+

## 📚 Additional Documentation

- **Full Guide**: See `KERALA_DATA_CREATION_GUIDE.md` for detailed documentation
- **District Mapping**: See `kerala_district_mapping.py` for district structure
- **OpenDataKerala**: https://opendatakerala.org/
- **Map Kerala**: https://map.opendatakerala.org/

## 🤝 Contributing

### Adding Missing LSGs

The `kerala_district_mapping.py` file currently has major LSGs (corporations, municipalities, block panchayats) but is missing most Grama Panchayats (941 total).

To add them:

1. Edit `kerala_district_mapping.py`
2. Add Grama Panchayat names under the appropriate district
3. Run Script 1 again to update the mapping

Example:
```python
"Thiruvananthapuram": {
    "corporations": [...],
    "municipalities": [...],
    "block_panchayats": [...],
    "grama_panchayats": [  # Add this section
        "Amboori Grama Panchayat",
        "Andoorkonam Grama Panchayat",
        # ... add all Grama Panchayats
    ]
}
```

### Adding Officials Data

Help collect officials data:
1. Fork this repository
2. Add data to `lsg_officials.csv`
3. Verify with multiple sources
4. Submit pull request
5. Include source references

## 🐛 Troubleshooting

### Issue: "File not found: kerala_lsg_data.geojson"
**Solution**: Run `./setup.sh` first to download the data

### Issue: "geopandas not installed"
**Solution**: 
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "district field not found"
**Solution**: Run scripts in order (1 → 2 → 3 → 4 → 5)

### Issue: GeoJSON too large
**Solution**: Increase simplification tolerance in Script 3:
```python
# In scripts/03_simplify_geojson.py
tolerance=0.005  # Try 0.01 for even more simplification
```

## 📄 License

- **Code**: MIT License (or GPL-3.0 to match BLR City Officials)
- **Data**: Open Database License (ODbL) - from OpenDataKerala
- **Officials Data**: Verify licensing before publishing

## 📧 Questions?

- Create an issue in this repository
- Contact OpenDataKerala community
- Join OSM Kerala discussions

## 🎯 Next Steps

After generating the data:

1. **Build Web Application**
   - Use Svelte/SvelteKit (like BLR City Officials)
   - Or React/Next.js
   - Or vanilla HTML/JS

2. **Deploy**
   - Vercel
   - Netlify
   - GitHub Pages

3. **Keep Data Updated**
   - Set up quarterly update schedule
   - Enable community contributions
   - Track data changes with Git

4. **Add Features**
   - Multi-language support (English/Malayalam)
   - Ward boundaries
   - Government office locations
   - Service center information

## 🌐 Web Application

The interactive map is built with SvelteKit and MapLibre GL JS.

### 1. Initial Setup
If you haven't run the setup script yet:
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Prepare Data
Run the processing pipeline to generate the necessary GeoJSON and search index files. This also syncs the data to the web app:
```bash
source venv/bin/activate
./run_all.sh
```

### 3. Start Development Server
```bash
cd web-app
npm install  # First time only
npm run dev
```
The website will be available at `http://localhost:5173`.

---

**Ready to build Kerala's civic engagement platform! 🚀**
