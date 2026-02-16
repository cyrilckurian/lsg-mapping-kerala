#!/bin/bash
# Kerala Officials Map - Complete Setup Script

set -e  # Exit on error

echo "========================================="
echo "Kerala Officials Map - Setup Script"
echo "========================================="
echo ""

# Create directory structure
echo "Creating directory structure..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p scripts
mkdir -p static/geojson

# Download LSG data from OpenDataKerala
echo ""
echo "Downloading Kerala LSG boundary data..."
cd data/raw

if [ ! -f kerala_lsg_data.geojson ]; then
    echo "Downloading from OpenDataKerala GitHub..."
    wget -O kerala_lsg_data.geojson \
        https://raw.githubusercontent.com/opendatakerala/lsg-kerala-data/main/data/kerala_lsg_data.geojson \
        || curl -L -o kerala_lsg_data.geojson \
        https://raw.githubusercontent.com/opendatakerala/lsg-kerala-data/main/data/kerala_lsg_data.geojson
    
    if [ -f kerala_lsg_data.geojson ]; then
        echo "✓ Successfully downloaded Kerala LSG data"
        file_size=$(du -h kerala_lsg_data.geojson | cut -f1)
        echo "  File size: $file_size"
    else
        echo "✗ Failed to download. Please download manually from:"
        echo "  https://github.com/opendatakerala/lsg-kerala-data/releases"
        exit 1
    fi
else
    echo "✓ Kerala LSG data already exists"
fi

cd ../..

# Check Python version
echo ""
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Detected: Python $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 14 ]; then
    echo "⚠️  NOTE: Python 3.14+ detected"
    echo "   Ensure you are using modern versions of pandas/geopandas (included in updated requirements.txt)"
    echo ""
    echo "RECOMMENDED: Use Python 3.11, 3.12, or 3.13 if you face build issues."
    echo ""
    # Removing the exit prompt to allow automation, assuming updated requirements work
fi

# Create Python virtual environment
echo ""
echo "Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Created virtual environment"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip

# Try to install dependencies
if pip install -r requirements.txt; then
    echo "✓ Dependencies installed"
else
    echo ""
    echo "❌ Installation failed"
    echo ""
    echo "This is likely due to Python 3.14 compatibility issues."
    echo ""
    echo "SOLUTION:"
    echo "  1. Install Python 3.13:"
    echo "     brew install python@3.13"
    echo ""
    echo "  2. Create venv with Python 3.13:"
    echo "     python3.13 -m venv venv"
    echo ""
    echo "  3. Run setup again:"
    echo "     ./setup.sh"
    exit 1
fi

# Create CSV template for officials data
echo ""
echo "Creating CSV template for officials data..."
cat > data/raw/lsg_officials_template.csv << 'EOF'
lsg_id,lsg_name,lsg_name_ml,lsg_type,district,president_name,president_party,president_contact,president_email,secretary_name,secretary_contact,secretary_email,office_address,website,wikidata_id,mla_constituency,mp_constituency,notes
KL-TVM-001,Thiruvananthapuram Corporation,തിരുവനന്തപുരം കോർപ്പറേഷൻ,corporation,Thiruvananthapuram,,,,,,,,,https://trivandrum.corporation.kerala.gov.in/,Q2095612,,,
KL-KLM-001,Kollam Corporation,കൊല്ലം കോർപ്പറേഷൻ,corporation,Kollam,,,,,,,,,https://www.kollammunicipalcorporation.in/,Q867715,,,
KL-KCH-001,Kochi Corporation,കൊച്ചി കോർപ്പറേഷൻ,corporation,Ernakulam,,,,,,,,,https://corporationofcochin.kerala.gov.in/,Q1626481,,,
KL-TSR-001,Thrissur Corporation,തൃശൂർ കോർപ്പറേഷൻ,corporation,Thrissur,,,,,,,,,https://www.thrissur.corporation.kerala.gov.in/,Q585712,,,
KL-KKD-001,Kozhikode Corporation,കോഴിക്കോട് കോർപ്പറേഷൻ,corporation,Kozhikode,,,,,,,,,https://kozhikodecorporation.net/,Q2042993,,,
KL-KNR-001,Kannur Corporation,കണ്ണൂർ കോർപ്പറേഷൻ,corporation,Kannur,,,,,,,,,https://kannur.corporation.kerala.gov.in/,Q2598894,,,
EOF

echo "✓ Created template: data/raw/lsg_officials_template.csv"

# Create README
echo ""
echo "Creating documentation..."
cat > data/README.md << 'EOF'
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
EOF

# Summary
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Check downloaded data:"
echo "   ls -lh data/raw/"
echo ""
echo "3. Fill in officials data:"
echo "   Edit: data/raw/lsg_officials_template.csv"
echo ""
echo "4. Run processing scripts:"
echo "   python scripts/01_add_district_field.py"
echo "   python scripts/02_extract_districts.py"
echo "   python scripts/03_simplify_geojson.py"
echo "   python scripts/04_merge_officials_data.py"
echo "   python scripts/05_generate_search_index.py"
echo ""
echo "Data Sources:"
echo "- Geographic: https://github.com/opendatakerala/lsg-kerala-data"
echo "- Officials: https://lsgkerala.gov.in/"
echo ""
