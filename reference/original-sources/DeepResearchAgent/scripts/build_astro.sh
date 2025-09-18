#!/bin/bash
# Astro Documentation Build and Deploy Script
# Parallel to existing documentation system - cost-optimized approach

set -e  # Exit on any error

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ASTRO_DIR="${REPO_ROOT}/astro-docs"
BUILD_DIR="${ASTRO_DIR}/dist"
GITHUB_PAGES_BRANCH="astro-docs"
REMOTE_NAME="origin"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[ASTRO INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[ASTRO SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[ASTRO WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ASTRO ERROR]${NC} $1"
}

# Check requirements
check_requirements() {
    log_info "Checking Astro build requirements..."

    # Check if we're in the right directory
    if [ ! -f "${REPO_ROOT}/astro-docs/package.json" ]; then
        log_error "Astro project not found. Make sure astro-docs/ directory exists."
        exit 1
    fi

    # Check Node.js
    if ! command -v node >/dev/null 2>&1; then
        log_error "Node.js is required but not installed."
        exit 1
    fi

    # Check npm
    if ! command -v npm >/dev/null 2>&1; then
        log_error "npm is required but not installed."
        exit 1
    fi

    log_success "All requirements met"
}

# Install dependencies if needed
install_dependencies() {
    log_info "Checking Astro dependencies..."

    cd "${ASTRO_DIR}"

    if [ ! -d "node_modules" ]; then
        log_info "Installing dependencies..."
        npm install
        log_success "Dependencies installed"
    else
        log_info "Dependencies already installed"
    fi
}

# Build the Astro site
build_astro() {
    log_info "Building Astro documentation site..."

    cd "${ASTRO_DIR}"

    # Measure build time
    start_time=$(date +%s)

    # Build the site
    if npm run build; then
        end_time=$(date +%s)
        build_time=$((end_time - start_time))
        log_success "Astro build completed in ${build_time} seconds"
    else
        log_error "Astro build failed"
        exit 1
    fi

    # Verify build output
    if [ ! -d "${BUILD_DIR}" ]; then
        log_error "Build directory not found after build"
        exit 1
    fi

    log_info "Build output location: ${BUILD_DIR}"
    log_info "Build size: $(du -sh "${BUILD_DIR}" | cut -f1)"
}

# Deploy to GitHub Pages (separate branch)
deploy_to_github() {
    log_info "Deploying Astro documentation to GitHub Pages..."

    # Store current branch
    current_branch=$(git branch --show-current)

    # Check if astro-docs branch exists
    if git show-ref --verify --quiet refs/heads/"${GITHUB_PAGES_BRANCH}"; then
        log_info "Astro docs branch exists"
    else
        log_info "Creating Astro docs branch..."
        git checkout --orphan "${GITHUB_PAGES_BRANCH}"
        git rm -rf . 2>/dev/null || true
        echo "# Astro Documentation" > README.md
        git add README.md
        git commit -m "Initial Astro documentation branch"
        git checkout "$current_branch"
    fi

    # Switch to astro-docs branch
    git checkout "${GITHUB_PAGES_BRANCH}"

    # Clear existing content (except .git)
    find . -maxdepth 1 -not -name '.git' -not -name '.' -exec rm -rf {} + 2>/dev/null || true

    # Copy built files
    if [ -d "${BUILD_DIR}" ] && [ "$(ls -A "${BUILD_DIR}")" ]; then
        cp -r "${BUILD_DIR}"/* .

        # Create CNAME for custom domain (if needed)
        # echo "docs.deepresearchagent.com" > CNAME

        # Add .nojekyll to prevent GitHub Pages Jekyll processing
        touch .nojekyll

        log_success "Astro files copied to deployment branch"
    else
        log_error "Build directory is empty or doesn't exist"
        git checkout "$current_branch"
        return 1
    fi

    # Add and commit
    git add .
    if git commit -m "Deploy Astro documentation - $(date)" 2>/dev/null; then
        log_info "Pushing to GitHub Pages..."

        # Push to GitHub
        if git push "${REMOTE_NAME}" "${GITHUB_PAGES_BRANCH}"; then
            log_success "Astro documentation deployed to GitHub Pages"
            log_info "Site should be available at: https://kairin.github.io/DeepResearchAgent/"
        else
            log_error "Failed to push to GitHub"
            git checkout "$current_branch"
            return 1
        fi
    else
        log_warning "No changes to deploy"
    fi

    # Return to original branch
    git checkout "$current_branch"
    log_success "Returned to ${current_branch} branch"
}

# Performance benchmarking
benchmark_performance() {
    log_info "Running performance analysis..."

    cd "${ASTRO_DIR}"

    # Count content files
    content_files=$(find src/content -name "*.md" 2>/dev/null | wc -l)
    log_info "Content files processed: ${content_files}"

    # Analyze bundle size
    if [ -d "${BUILD_DIR}" ]; then
        total_size=$(du -sh "${BUILD_DIR}" | cut -f1)
        js_size=$(find "${BUILD_DIR}" -name "*.js" -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1 || echo "0")
        css_size=$(find "${BUILD_DIR}" -name "*.css" -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1 || echo "0")

        log_info "Performance metrics:"
        log_info "  Total build size: ${total_size}"
        log_info "  JavaScript size: ${js_size}"
        log_info "  CSS size: ${css_size}"
        log_info "  Content files: ${content_files}"
    fi
}

# Main execution
main() {
    log_info "Starting Astro documentation build process..."

    check_requirements
    install_dependencies
    build_astro
    benchmark_performance

    if [[ "${1:-}" == "--deploy" ]]; then
        deploy_to_github
        log_success "Build and deploy completed successfully!"
        log_info "Astro documentation site deployed to separate GitHub Pages branch"
    else
        log_success "Build completed successfully!"
        log_info "Built files are in: ${BUILD_DIR}"
        log_info "To deploy to GitHub Pages, run: $0 --deploy"
    fi

    log_info "Astro documentation system ready for development"
}

# Run main function
main "$@"