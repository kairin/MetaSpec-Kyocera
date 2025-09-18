#!/bin/bash
# Auto-build Astro site when research data changes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ASTRO_DIR="$PROJECT_ROOT/astro-docs"

echo "🔄 Auto-building Astro site..."

# Update research data
echo "📊 Updating research data..."
cd "$PROJECT_ROOT"
uv run python scripts/astro_data_pipeline.py

# Sync documentation from main project
echo "📚 Syncing documentation..."
# Copy latest documentation updates if needed
# (Main docs are already organized in astro-docs/src/content/docs/)

# Check if Astro directory exists
if [ ! -d "$ASTRO_DIR" ]; then
    echo "❌ Astro directory not found: $ASTRO_DIR"
    exit 1
fi

# Change to Astro directory
cd "$ASTRO_DIR"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Astro dependencies..."
    npm install
fi

# Build the site
echo "🏗️  Building Astro site..."
npm run build

# Start dev server if requested
if [ "$1" = "--dev" ]; then
    echo "🚀 Starting Astro dev server..."
    npm run dev
else
    echo "✅ Astro site built successfully!"
    echo "📁 Build output available in: $ASTRO_DIR/dist"
    echo ""
    echo "To preview the site:"
    echo "  cd $ASTRO_DIR"
    echo "  npm run preview"
    echo ""
    echo "To start development server:"
    echo "  ./scripts/auto_build_astro.sh --dev"
fi