#!/bin/bash
set -e

echo "🚀 Running GitHub Actions workflow locally using gh CLI..."

# Ensure we're in the project root
cd "$(dirname "$0")/../.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_section() {
    echo -e "\n${BLUE}🔧 $1${NC}"
    echo "================================================="
}

# Check if gh CLI is installed and authenticated
print_section "Checking GitHub CLI setup"

if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed. Please install it first:"
    echo "  https://cli.github.com/"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    print_error "GitHub CLI is not authenticated. Please run:"
    echo "  gh auth login"
    exit 1
fi

print_status "GitHub CLI is installed and authenticated"

# Check current repository
REPO_INFO=$(gh repo view --json nameWithOwner,defaultBranchRef --jq '{name: .nameWithOwner, branch: .defaultBranchRef.name}')
REPO_NAME=$(echo "$REPO_INFO" | jq -r '.name')
DEFAULT_BRANCH=$(echo "$REPO_INFO" | jq -r '.branch')

print_info "Repository: $REPO_NAME"
print_info "Default branch: $DEFAULT_BRANCH"

# Function to simulate workflow environment
simulate_github_env() {
    print_section "Setting up GitHub Actions environment variables"

    export GITHUB_WORKSPACE="$(pwd)"
    export GITHUB_REPOSITORY="$REPO_NAME"
    export GITHUB_REF="refs/heads/$DEFAULT_BRANCH"
    export GITHUB_SHA="$(git rev-parse HEAD)"
    export GITHUB_ACTOR="$(gh api user --jq '.login')"
    export GITHUB_EVENT_NAME="push"
    export RUNNER_OS="Linux"
    export RUNNER_ARCH="X64"

    print_status "Environment variables set"
    echo "  GITHUB_WORKSPACE: $GITHUB_WORKSPACE"
    echo "  GITHUB_REPOSITORY: $GITHUB_REPOSITORY"
    echo "  GITHUB_REF: $GITHUB_REF"
    echo "  GITHUB_SHA: $GITHUB_SHA"
    echo "  GITHUB_ACTOR: $GITHUB_ACTOR"
}

# Function to run workflow steps locally
run_workflow_locally() {
    print_section "Running workflow steps locally"

    # Step 1: Checkout (already in correct directory)
    print_status "Step 1: Checkout - Already in repository directory"

    # Step 2: Setup Node.js
    print_info "Step 2: Setup Node.js"
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi

    NODE_VERSION=$(node --version)
    print_status "Node.js version: $NODE_VERSION"

    # Step 3: Install dependencies
    print_info "Step 3: Install dependencies"
    if [ ! -d "web" ]; then
        print_error "Web directory not found"
        exit 1
    fi

    cd web
    if [ ! -f "package.json" ]; then
        print_error "package.json not found in web directory"
        exit 1
    fi

    print_info "Installing npm dependencies..."
    # Always use npm install with legacy-peer-deps to avoid sync issues
    npm install --legacy-peer-deps
    cd ..

    # Step 4: Prepare documentation
    print_info "Step 4: Prepare documentation for Astro"
    mkdir -p web/src/pages/docs

    # Copy main documentation files
    cp README.md web/src/pages/docs/readme.md
    cp AGENTS.md web/src/pages/docs/agents.md

    # Copy documentation structure
    if [ -d "docs" ]; then
        cp -r docs/* web/src/pages/docs/
        print_status "Documentation files copied"
    fi

    # Create navigation structure
    cat > web/src/pages/docs/navigation.json << 'EOF'
{
  "sections": [
    {"title": "Overview", "items": [
      {"title": "Project README", "path": "/docs/readme"},
      {"title": "LLM Instructions", "path": "/docs/agents"}
    ]},
    {"title": "Planning", "items": [
      {"title": "System Planning", "path": "/docs/planning/system-planning"}
    ]},
    {"title": "Implementation", "items": [
      {"title": "Phase 1 Foundation", "path": "/docs/implementation/phase-1-foundation"}
    ]},
    {"title": "Architecture", "items": [
      {"title": "Web Interface", "path": "/docs/architecture/web-interface-integration"}
    ]},
    {"title": "User Guides", "items": [
      {"title": "Getting Started", "path": "/docs/user-guides/getting-started"}
    ]},
    {"title": "Development", "items": [
      {"title": "Development Setup", "path": "/docs/development/development-setup"}
    ]},
    {"title": "API Reference", "items": [
      {"title": "API Overview", "path": "/docs/api/api-overview"}
    ]}
  ]
}
EOF

    # Step 5: Build with Astro
    print_info "Step 5: Build with Astro"
    cd web
    npm run build
    cd ..

    print_status "Local workflow completed successfully!"
}

# Function to check workflow status on GitHub
check_github_workflows() {
    print_section "Checking GitHub Actions workflow status"

    # List recent workflow runs
    gh run list --limit 5 --json status,conclusion,name,createdAt,url --jq '.[] | {name: .name, status: .status, conclusion: .conclusion, created: .createdAt, url: .url}'

    # Check if there are any failed workflows
    FAILED_RUNS=$(gh run list --status failure --limit 1 --json name --jq '.[].name // empty')
    if [ -n "$FAILED_RUNS" ]; then
        print_warning "There are failed workflow runs. Use 'gh run view' to see details."
    fi
}

# Function to trigger workflow on GitHub
trigger_github_workflow() {
    print_section "Triggering workflow on GitHub"

    if gh workflow list --json name,state --jq '.[] | select(.name == "Deploy Documentation")' > /dev/null; then
        print_info "Triggering 'Deploy Documentation' workflow..."
        gh workflow run "Deploy Documentation"
        print_status "Workflow triggered. Check status with: gh run list"
    else
        print_warning "Deploy Documentation workflow not found"
        gh workflow list
    fi
}

# Function to enable GitHub Pages
enable_github_pages() {
    print_section "Enabling GitHub Pages"

    # Check if Pages is already enabled
    if gh api "repos/$REPO_NAME/pages" &> /dev/null; then
        print_status "GitHub Pages is already enabled"
        gh api "repos/$REPO_NAME/pages" --jq '{status: .status, url: .html_url, source: .source}'
    else
        print_info "Enabling GitHub Pages with GitHub Actions source..."
        gh api "repos/$REPO_NAME/pages" -X POST -f build_type='workflow' || {
            print_warning "Could not enable GitHub Pages automatically. Please enable it manually:"
            echo "  1. Go to repository Settings > Pages"
            echo "  2. Set source to 'GitHub Actions'"
            echo "  3. Save the configuration"
        }
    fi
}

# Main execution flow
main() {
    print_section "GitHub CLI Local Workflow Runner"
    echo "This script runs GitHub Actions workflows locally using gh CLI"
    echo ""

    # Parse command line arguments
    case "${1:-local}" in
        "local")
            simulate_github_env
            run_workflow_locally
            ;;
        "status")
            check_github_workflows
            ;;
        "trigger")
            trigger_github_workflow
            ;;
        "pages")
            enable_github_pages
            ;;
        "all")
            simulate_github_env
            run_workflow_locally
            enable_github_pages
            trigger_github_workflow
            check_github_workflows
            ;;
        "help"|"-h"|"--help")
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  local     Run workflow locally (default)"
            echo "  status    Check GitHub workflow status"
            echo "  trigger   Trigger workflow on GitHub"
            echo "  pages     Enable GitHub Pages"
            echo "  all       Run local + enable pages + trigger + check status"
            echo "  help      Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0              # Run locally"
            echo "  $0 local        # Run locally"
            echo "  $0 status       # Check workflow status"
            echo "  $0 trigger      # Trigger on GitHub"
            echo "  $0 all          # Full workflow"
            exit 0
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac

    print_status "Script completed successfully!"
    echo ""
    echo "📖 Documentation available at:"
    echo "   Local: file://$(pwd)/web/dist/index.html"
    echo "   Dev server: cd web && npm run preview"
    echo "   GitHub Pages: https://$(echo $REPO_NAME | tr '[:upper:]' '[:lower:]' | sed 's/\//.github.io\//')"
    echo ""
}

# Run main function with all arguments
main "$@"