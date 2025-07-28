#!/bin/bash
# Script to build documentation

set -e

echo "🔧 Building Sphinx documentation..."

# Change to docs directory
cd "$(dirname "$0")"

# Clean previous build
if [ -d "_build" ]; then
    echo "🧹 Cleaning previous build..."
    rm -rf _build
fi

# Build HTML documentation
echo "📚 Building HTML documentation..."
poetry run sphinx-build -b html . _build/html

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Documentation built successfully!"
    echo "📖 Open docs/_build/html/index.html in your browser to view"
    echo ""
    echo "🌐 To serve locally:"
    echo "   cd docs/_build/html && python -m http.server 8000"
    echo "   Then open http://localhost:8000"
else
    echo "❌ Documentation build failed!"
    exit 1
fi
