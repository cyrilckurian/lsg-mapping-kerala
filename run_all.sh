#!/bin/bash
# Run All Processing Scripts in Sequence

set -e  # Exit on error

echo "========================================="
echo "Kerala Officials Map - Processing Pipeline"
echo "========================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated"
    echo "Please run: source venv/bin/activate"
    echo "Or run ./setup.sh first if you haven't already"
    exit 1
fi

# Check if raw data exists
if [ ! -f "data/raw/kerala_lsg_data.geojson" ]; then
    echo "❌ Kerala LSG data not found"
    echo "Please run ./setup.sh first to download the data"
    exit 1
fi

echo "✓ Environment ready"
echo ""

# Script 1: Add district field
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1/5: Adding district field to LSG data"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python scripts/01_add_district_field.py
if [ $? -ne 0 ]; then
    echo "❌ Script 1 failed"
    exit 1
fi
echo ""

# Script 2: Extract districts
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2/5: Extracting district boundaries"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python scripts/02_extract_districts.py
if [ $? -ne 0 ]; then
    echo "❌ Script 2 failed"
    exit 1
fi
echo ""

# Script 3: Simplify
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3/5: Simplifying GeoJSON for web"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python scripts/03_simplify_geojson.py
if [ $? -ne 0 ]; then
    echo "❌ Script 3 failed"
    exit 1
fi
echo ""

# Check if officials data exists
if [ -f "data/raw/lsg_officials.csv" ]; then
    HAS_OFFICIALS=true
    echo "✓ Officials data found"
elif [ -f "data/raw/lsg_officials_template.csv" ]; then
    HAS_OFFICIALS=false
    echo "⚠️  Using template file (no actual officials data)"
else
    HAS_OFFICIALS=false
    echo "⚠️  No officials data found"
fi
echo ""

# Script 4: Merge officials (if available)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4/5: Merging officials data"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python scripts/04_merge_officials_data.py
if [ $? -ne 0 ]; then
    echo "⚠️  Script 4 failed (this is OK if you don't have officials data yet)"
    echo "   You can still use the GeoJSON without officials data"
    echo "   Add officials data later and re-run this script"
    SKIP_SEARCH=true
else
    SKIP_SEARCH=false
fi
echo ""

# Script 5: Generate search index
if [ "$SKIP_SEARCH" = false ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Step 5/5: Generating search index"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python scripts/05_generate_search_index.py
    if [ $? -ne 0 ]; then
        echo "❌ Script 5 failed"
        exit 1
    fi
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Step 5/5: Skipping search index (no final data)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi
echo ""

# Summary
echo "========================================="
echo "PROCESSING COMPLETE!"
echo "========================================="
echo ""
echo "Generated files:"
echo "  ✓ data/processed/kerala_lsg_with_districts.geojson"
echo "  ✓ data/processed/kerala_districts.geojson"
echo "  ✓ data/processed/kerala_lsg_simplified.geojson"
echo "  ✓ data/processed/kerala_districts_simplified.geojson"

if [ "$SKIP_SEARCH" = false ]; then
    echo "  ✓ data/processed/kerala_lsg_final.geojson"
    echo "  ✓ data/processed/search_index.json"
else
    echo "  ⚠️  kerala_lsg_final.geojson (partial - no officials data)"
    echo "  ⚠️  search_index.json (not generated)"
fi

echo ""
echo "File sizes:"
ls -lh data/processed/*.geojson data/processed/*.json 2>/dev/null | awk '{print "  " $9 " - " $5}'

echo ""
echo "Next steps:"
echo ""

if [ "$HAS_OFFICIALS" = false ]; then
    echo "📝 Add officials data:"
    echo "   1. Copy template: cp data/raw/lsg_officials_template.csv data/raw/lsg_officials.csv"
    echo "   2. Fill in officials information"
    echo "   3. Re-run: ./run_all.sh"
    echo ""
fi

echo "🌐 Use in web application:"
echo "   - kerala_lsg_final.geojson - Main map layer"
echo "   - kerala_districts_simplified.geojson - Base layer"
echo "   - search_index.json - Search functionality"
echo ""

# Automated copy to web app
echo "Syncing data with web application..."
mkdir -p web-app/static/data
cp data/processed/kerala_lsg_final.geojson web-app/static/data/
cp data/processed/kerala_districts.geojson web-app/static/data/
cp data/processed/search_index.json web-app/static/data/
# Copy Mahe if exists
if [ -f data/raw/mahe_boundary.geojson ]; then
    cp data/raw/mahe_boundary.geojson web-app/static/data/
fi
echo "✓ Data synced to web-app/static/data/"
echo ""

echo "📖 See README.md for integration examples"
echo ""
