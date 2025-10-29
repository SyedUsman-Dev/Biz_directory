#!/bin/bash

echo "Exporting MongoDB collections for assignment submission..."
echo ""

python export_data.py

echo ""
echo "Creating submission ZIP file..."
cd exports && zip -q ../biz-directory-mongodb.zip *.json && cd ..
echo "✓ Created biz-directory-mongodb.zip"
echo ""
echo "Ready for submission!"
