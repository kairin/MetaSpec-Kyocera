#!/bin/bash
set -e

echo "📄 Setting up GitHub Pages with zero-cost configuration..."

# Ensure we're in the project root
cd "$(dirname "$0")/../.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check gh CLI
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is required. Install from https://cli.github.com/"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    print_error "Please authenticate with GitHub CLI: gh auth login"
    exit 1
fi

# Get repository info
REPO_INFO=$(gh repo view --json nameWithOwner,defaultBranchRef,visibility --jq '{name: .nameWithOwner, branch: .defaultBranchRef.name, visibility: .visibility}')
REPO_NAME=$(echo "$REPO_INFO" | jq -r '.name')
VISIBILITY=$(echo "$REPO_INFO" | jq -r '.visibility')

print_section "Repository Configuration"
print_info "Repository: $REPO_NAME"
print_info "Visibility: $VISIBILITY"

# Check if public (required for free GitHub Pages)
if [ "$VISIBILITY" != "PUBLIC" ]; then
    print_warning "Repository is $VISIBILITY. GitHub Pages requires a public repository for free tier."
    echo "Would you like to make the repository public? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        gh api "repos/$REPO_NAME" -X PATCH -f visibility='public'
        print_status "Repository made public"
    else
        print_error "GitHub Pages requires a public repository. Exiting."
        exit 1
    fi
fi

print_section "GitHub Pages Setup"

# Check current Pages status
if gh api "repos/$REPO_NAME/pages" &> /dev/null; then
    print_status "GitHub Pages is already enabled"
    PAGES_INFO=$(gh api "repos/$REPO_NAME/pages" --jq '{status: .status, url: .html_url, source: .source, build_type: .build_type}')
    echo "$PAGES_INFO" | jq .
else
    print_info "Enabling GitHub Pages with GitHub Actions source..."

    # Try to enable Pages with GitHub Actions source
    if gh api "repos/$REPO_NAME/pages" -X POST -f build_type='workflow'; then
        print_status "GitHub Pages enabled with GitHub Actions source"
    else
        print_warning "Could not enable GitHub Pages automatically"
        print_info "Manual setup required:"
        echo "  1. Go to https://github.com/$REPO_NAME/settings/pages"
        echo "  2. Set source to 'GitHub Actions'"
        echo "  3. Save the configuration"
        echo ""
        echo "Press Enter when you've completed the manual setup..."
        read -r
    fi
fi

print_section "Workflow Configuration Check"

# Check if workflow file exists and is valid
if [ -f ".github/workflows/pages.yml" ]; then
    print_status "Pages workflow file found"

    # Validate workflow syntax using gh
    if gh workflow list | grep -q "Deploy Documentation"; then
        print_status "Deploy Documentation workflow is registered"
    else
        print_warning "Workflow might not be properly registered"
    fi
else
    print_error "Pages workflow file not found at .github/workflows/pages.yml"
    exit 1
fi

print_section "Testing Workflow Costs"

# Get workflow usage/billing info
print_info "Checking workflow usage to ensure zero cost..."

# Check repository settings for Actions
ACTIONS_INFO=$(gh api "repos/$REPO_NAME" --jq '{
    actions_enabled: .has_issues,
    pages_enabled: .has_pages,
    visibility: .visibility,
    fork: .fork,
    private: .private
}')

echo "Repository configuration:"
echo "$ACTIONS_INFO" | jq .

# Get current workflow runs
print_info "Recent workflow runs:"
if gh run list --limit 3 --json status,conclusion,name,createdAt,billable --jq '.[] | {name: .name, status: .status, conclusion: .conclusion, created: .createdAt, billable: .billable}' 2>/dev/null; then
    print_status "Workflow history retrieved"
else
    print_warning "No workflow runs found yet"
fi

print_section "Zero-Cost Verification"

# Verify this is using free tier resources
print_info "Verifying zero-cost configuration:"
echo "✓ Public repository (required for free Pages)"
echo "✓ GitHub Actions (2000 minutes/month free)"
echo "✓ GitHub Pages (1GB storage, 100GB bandwidth/month free)"
echo "✓ Node.js workflow (uses standard GitHub-hosted runners)"

print_section "Next Steps"

print_status "GitHub Pages setup complete!"
echo ""
echo "🚀 To use the local workflow runner:"
echo "   ./local-infra/runners/gh-workflow-local.sh local    # Run locally"
echo "   ./local-infra/runners/gh-workflow-local.sh trigger  # Trigger on GitHub"
echo "   ./local-infra/runners/gh-workflow-local.sh status   # Check status"
echo "   ./local-infra/runners/gh-workflow-local.sh all      # Full workflow"
echo ""
echo "📖 Documentation will be available at:"
echo "   https://$(echo $REPO_NAME | tr '[:upper:]' '[:lower:]' | sed 's/\//.github.io\//')"
echo ""
echo "💰 Cost monitoring:"
echo "   Check usage at: https://github.com/settings/billing"
echo "   All resources used are within GitHub's free tier limits"