#!/bin/bash
# Local CI/CD Pipeline for DeepResearchAgent
# Run this script regularly to ensure repository integrity

set -e

echo "🚀 Starting Local CI/CD Pipeline for DeepResearchAgent"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check git status
echo "🔍 Checking git status..."
if [[ -n $(git status --porcelain) ]]; then
    print_error "Working directory is not clean. Please commit or stash changes."
    git status
    exit 1
fi
print_status "Working directory is clean"

# Check if on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    print_warning "Not on main branch (currently on: $CURRENT_BRANCH)"
    echo "Switching to main branch..."
    git checkout main
fi
print_status "On main branch"

# Fetch latest changes
echo "📥 Fetching latest changes..."
git fetch --all --quiet
print_status "Fetched latest changes"

# Check for upstream changes
UPSTREAM_CHANGES=$(git log --oneline HEAD..upstream/main 2>/dev/null | wc -l)
if [[ $UPSTREAM_CHANGES -gt 0 ]]; then
    print_warning "Found $UPSTREAM_CHANGES upstream changes"
    echo "Upstream changes:"
    git log --oneline HEAD..upstream/main | head -5
    echo ""
    read -p "Do you want to sync with upstream? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 Syncing with upstream..."
        ./scripts/sync_upstream.sh
    fi
else
    print_status "No upstream changes detected"
fi

# Run migration validation
echo "🔍 Running migration validation..."
if uv run python scripts/validate_migration.py; then
    print_status "Migration validation passed"
else
    print_error "Migration validation failed"
    exit 1
fi

# Run comprehensive tests
echo "🧪 Running comprehensive test suite..."
if uv run python scripts/run_comprehensive_tests.py --unit-only; then
    print_status "Unit tests passed"
else
    print_error "Unit tests failed"
    exit 1
fi

# Check for security vulnerabilities
echo "🔒 Checking for security vulnerabilities..."
if uv run pip-audit --quiet; then
    print_status "No security vulnerabilities found"
else
    print_warning "Security vulnerabilities detected (check output above)"
fi

# Validate dependencies
echo "📦 Validating dependencies..."
if uv lock --check; then
    print_status "Dependencies are valid"
else
    print_error "Dependency validation failed"
    exit 1
fi

# Run linting
echo "🧹 Running linting checks..."
if uv run ruff check . --quiet; then
    print_status "Linting passed"
else
    print_warning "Linting issues found"
fi

# Check formatting
echo "🎨 Checking code formatting..."
if uv run black --check . --quiet && uv run isort --check-only . --quiet; then
    print_status "Code formatting is correct"
else
    print_warning "Code formatting issues found"
fi

# Test basic imports
echo "🔧 Testing basic imports..."
if uv run python -c "import src; print('Core import successful')"; then
    print_status "Basic imports working"
else
    print_error "Basic imports failed"
    exit 1
fi

# Create timestamped backup
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_BRANCH="backup-ci-${TIMESTAMP}"
echo "💾 Creating backup branch: $BACKUP_BRANCH"
git checkout -b "$BACKUP_BRANCH" --quiet
git checkout main --quiet
print_status "Backup created: $BACKUP_BRANCH"

# Final summary
echo ""
echo "=================================================="
echo "🎉 Local CI/CD Pipeline Completed Successfully!"
echo "=================================================="
echo ""
echo "📊 Summary:"
echo "  ✅ Git status: Clean"
echo "  ✅ Branch: main"
echo "  ✅ Migration: Validated"
echo "  ✅ Tests: Passed"
echo "  ✅ Security: Checked"
echo "  ✅ Dependencies: Valid"
echo "  ✅ Linting: Completed"
echo "  ✅ Formatting: Checked"
echo "  ✅ Imports: Working"
echo "  ✅ Backup: Created ($BACKUP_BRANCH)"
echo ""
echo "🔄 Next run: $(date -d '+24 hours' '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "💡 Tips:"
echo "  - Run this script daily or before major changes"
echo "  - Check test_output/ for detailed logs"
echo "  - Use archive branches for all changes (see AGENTS.md)"
echo "  - Never commit directly to main"