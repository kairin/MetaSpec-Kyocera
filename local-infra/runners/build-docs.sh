#!/bin/bash
set -e

echo "🏗️ Building MetaSpec-Kyocera Documentation Site..."

# Ensure we're in the project root
cd "$(dirname "$0")/../.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ to build documentation."
    exit 1
fi

# Check if we're in web directory
if [ ! -d "web" ]; then
    print_error "Web directory not found. Please run this script from the project root."
    exit 1
fi

print_status "Preparing documentation files for Astro build..."

# Create pages directory for documentation
mkdir -p web/src/pages/docs

# Copy main documentation files
cp README.md web/src/pages/docs/readme.md
cp AGENTS.md web/src/pages/docs/agents.md

# Copy documentation structure maintaining hierarchy
if [ -d "docs" ]; then
    cp -r docs/* web/src/pages/docs/
    print_status "Documentation files copied to Astro pages"
else
    print_warning "docs/ directory not found, skipping documentation copy"
fi

# Create navigation structure for documentation
cat > web/src/pages/docs/navigation.json << 'EOF'
{
  "title": "MetaSpec-Kyocera Documentation",
  "sections": [
    {
      "title": "Overview",
      "items": [
        {"title": "Project README", "path": "/docs/readme", "description": "Project overview and quick start"},
        {"title": "LLM Instructions", "path": "/docs/agents", "description": "Critical requirements for AI assistants"}
      ]
    },
    {
      "title": "Planning",
      "items": [
        {"title": "System Planning", "path": "/docs/planning/system-planning", "description": "Comprehensive system architecture and strategy"}
      ]
    },
    {
      "title": "Implementation",
      "items": [
        {"title": "Phase 1 Foundation", "path": "/docs/implementation/phase-1-foundation", "description": "Core infrastructure setup guide"}
      ]
    },
    {
      "title": "Architecture",
      "items": [
        {"title": "Web Interface", "path": "/docs/architecture/web-interface-integration", "description": "Frontend architecture details"}
      ]
    },
    {
      "title": "User Guides",
      "items": [
        {"title": "Getting Started", "path": "/docs/user-guides/getting-started", "description": "Quick start guide for end users"}
      ]
    },
    {
      "title": "Development",
      "items": [
        {"title": "Development Setup", "path": "/docs/development/development-setup", "description": "Complete development environment guide"}
      ]
    },
    {
      "title": "API Reference",
      "items": [
        {"title": "API Overview", "path": "/docs/api/api-overview", "description": "REST API documentation and examples"}
      ]
    }
  ]
}
EOF

print_status "Navigation structure created"

# Change to web directory
cd web

# Check if package.json exists
if [ ! -f "package.json" ]; then
    print_error "package.json not found in web directory. Please run npm install first."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js dependencies..."
    npm ci
fi

print_status "Building Astro documentation site..."

# Build the Astro site
if npm run build; then
    print_status "Astro build completed successfully"
else
    print_error "Astro build failed"
    exit 1
fi

# Create a simple index.html redirect if it doesn't exist
if [ ! -f "dist/index.html" ]; then
    cat > dist/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MetaSpec-Kyocera Documentation</title>
    <meta http-equiv="refresh" content="0; url=/docs/readme">
    <link rel="canonical" href="/docs/readme">
</head>
<body>
    <p>Redirecting to <a href="/docs/readme">documentation</a>...</p>
</body>
</html>
EOF
    print_status "Created index.html redirect"
fi

# Copy built site to docs directory for GitHub Pages (if deploying to docs/)
if [ ! -d "../docs" ]; then
    mkdir -p ../docs
fi

# Copy built files to docs for GitHub Pages
cp -r dist/* ../docs/ 2>/dev/null || true

print_status "Documentation site built successfully!"
echo ""
echo "📖 Documentation available at:"
echo "   Local: file://$(pwd)/dist/index.html"
echo "   Dev server: npm run dev (from web/ directory)"
echo "   GitHub Pages: Will be available after push to main branch"
echo ""
echo "🚀 To serve locally:"
echo "   cd web && npm run preview"
echo ""

# Return to project root
cd ..

print_status "Build script completed successfully!"