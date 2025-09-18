#!/bin/bash
# Simple Documentation Build and Deploy Script
# Eliminates GitHub Actions costs by building locally and pushing only built files

set -e  # Exit on any error

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${REPO_ROOT}/build_docs"
GITHUB_PAGES_BRANCH="gh-pages"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Clean and create build directory
log_info "Setting up build directory..."
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# Create simple index.html
log_info "Creating documentation index..."
cat > "${BUILD_DIR}/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepResearchAgent Documentation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px; margin: 0 auto; padding: 20px;
            background: #1a1a1a; color: #e0e0e0; line-height: 1.6;
        }
        h1, h2 { color: #4a90e2; }
        .section {
            background: #2d2d2d; padding: 20px; margin: 20px 0;
            border-radius: 8px; border-left: 4px solid #4a90e2;
        }
        .grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px; margin: 20px 0;
        }
        .card {
            background: #3d3d3d; padding: 15px; border-radius: 6px;
            border: 1px solid #555;
        }
        .card a { color: #7dd3fc; text-decoration: none; font-weight: 500; }
        .card a:hover { text-decoration: underline; }
        .badge {
            background: #4a90e2; color: white; padding: 2px 8px;
            border-radius: 12px; font-size: 12px; margin-left: 10px;
        }
        .new { background: #10b981; }
        .core { background: #f59e0b; }
        .desc { font-size: 14px; color: #ccc; margin-top: 8px; }
    </style>
</head>
<body>
    <h1>🤖 DeepResearchAgent Documentation</h1>
    <p>Hierarchical Multi-Agent Framework for Research and Analysis</p>

    <div class="section">
        <h2>🚀 Quick Start</h2>
        <div class="grid">
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/AGENTS.md">📖 Main Documentation</a>
                <span class="badge core">Core</span>
                <div class="desc">Complete setup guide and usage instructions</div>
            </div>
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/CHANGELOG.md">📋 Changelog</a>
                <span class="badge">Updates</span>
                <div class="desc">Latest changes and version history</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🎯 TUI Development Planning</h2>
        <div class="grid">
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/planning/TUI_ANALYSIS_AND_STRATEGY.md">🔍 TUI Analysis & Strategy</a>
                <span class="badge new">New</span>
                <div class="desc">Comprehensive fault analysis and TUI development strategy</div>
            </div>
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/planning/tui/specifications/technical_requirements.md">⚙️ Technical Requirements</a>
                <span class="badge new">New</span>
                <div class="desc">Complete technical specifications for TUI implementation</div>
            </div>
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/planning/tui/specifications/implementation_phases.md">📅 Implementation Phases</a>
                <span class="badge new">New</span>
                <div class="desc">8-week phased development timeline</div>
            </div>
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/planning/tui/specifications/detailed_todo_checklist.md">✅ Implementation Checklist</a>
                <span class="badge new">New</span>
                <div class="desc">200+ detailed implementation tasks and requirements</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🏗️ System Architecture</h2>
        <div class="grid">
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/planning/tui/diagrams/system_architecture.md">📊 Architecture Diagrams</a>
                <span class="badge new">New</span>
                <div class="desc">Mermaid diagrams for TUI-Core system integration</div>
            </div>
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/planning/tui/mockups/interface_designs.svg">🎨 Interface Mockups</a>
                <span class="badge new">New</span>
                <div class="desc">Professional TUI interface design mockups</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📊 Development Reports</h2>
        <div class="grid">
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/session_reports/SESSION_2025-01-16_HUGGINGFACE_CLI_FIXES.md">🔧 HuggingFace & CLI Fixes</a>
                <span class="badge new">New</span>
                <div class="desc">Critical system fixes and CLI-first implementation</div>
            </div>
            <div class="card">
                <a href="https://github.com/kairin/DeepResearchAgent/blob/main/docs/development/GIT_STRATEGY.md">🌿 Git Strategy</a>
                <span class="badge">Process</span>
                <div class="desc">Archive-first git workflow documentation</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>💾 Local Build System</h2>
        <p>This documentation site is generated locally to eliminate GitHub Actions costs. The system includes:</p>
        <ul>
            <li>✅ <strong>Disabled GitHub Actions</strong> - No automatic CI/CD costs</li>
            <li>✅ <strong>Local Documentation Build</strong> - Generated using local scripts</li>
            <li>✅ <strong>Direct GitHub Links</strong> - Links to source files for latest content</li>
            <li>✅ <strong>Cost Optimization</strong> - Zero runner costs for documentation updates</li>
        </ul>
    </div>

    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #555; text-align: center; color: #888;">
        <p>🤖 DeepResearchAgent - Generated locally to prevent CI/CD costs</p>
        <p>📅 Last updated: $(date)</p>
    </footer>
</body>
</html>
EOF

# Deploy to GitHub Pages
log_info "Preparing deployment to GitHub Pages..."

# Store current branch
current_branch=$(git branch --show-current)

# Create or switch to gh-pages branch
if git show-ref --verify --quiet refs/heads/"${GITHUB_PAGES_BRANCH}"; then
    git checkout "${GITHUB_PAGES_BRANCH}"
else
    git checkout --orphan "${GITHUB_PAGES_BRANCH}"
    git rm -rf . 2>/dev/null || true
fi

# Clear existing content (except .git)
find . -maxdepth 1 -not -name '.git' -not -name '.' -exec rm -rf {} + 2>/dev/null || true

# Copy built files
cp "${BUILD_DIR}/index.html" .

# Add and commit
git add .
if git commit -m "Update documentation site - $(date)" 2>/dev/null; then
    log_info "Pushing to GitHub Pages..."
    git push origin "${GITHUB_PAGES_BRANCH}"
    log_success "Documentation deployed to GitHub Pages!"
    log_info "Site available at: https://kairin.github.io/DeepResearchAgent/"
else
    log_info "No changes to deploy"
fi

# Return to original branch
git checkout "$current_branch"

log_success "Build and deploy completed!"