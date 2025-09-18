#!/bin/bash
# Setup git protection mechanisms for fork-specific changes

set -e

echo "Setting up git protection for fork-specific changes..."

# Configure merge strategy for protected files
git config merge.ours.driver true

# Add upstream remote if it doesn't exist
if ! git remote get-url upstream >/dev/null 2>&1; then
    echo "Adding upstream remote..."
    git remote add upstream https://github.com/SkyworkAI/DeepResearchAgent.git
    echo "✅ Added upstream remote"
else
    echo "✅ Upstream remote already exists"
fi

# Create backup branch
BACKUP_BRANCH="backup-migration-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BACKUP_BRANCH"
git checkout -

echo "✅ Created backup branch: $BACKUP_BRANCH"

# Setup pre-merge hook
HOOKS_DIR=".git/hooks"
PRE_MERGE_HOOK="$HOOKS_DIR/pre-merge-commit"

mkdir -p "$HOOKS_DIR"

cat > "$PRE_MERGE_HOOK" << 'EOF'
#!/bin/bash
# Pre-merge validation hook

echo "🔍 Validating migration integrity before merge..."

# Check if this is a merge commit
if [ -f .git/MERGE_HEAD ]; then
    # Run validation
    if ! uv run python scripts/validate_migration.py; then
        echo "❌ Migration validation failed!"
        echo "Please fix issues before committing merge."
        exit 1
    fi
    echo "✅ Migration validation passed"
fi
EOF

chmod +x "$PRE_MERGE_HOOK"
echo "✅ Created pre-merge validation hook"

# Setup commit message template for merges
cat > ".gitmessage" << 'EOF'
Merge upstream changes while preserving uv migration

# Migration checklist:
# - [ ] Validated with: uv run python scripts/validate_migration.py
# - [ ] Tested core imports work
# - [ ] Verified uv commands still work
# - [ ] Checked for new Poetry references to convert
# - [ ] Updated any new installation instructions to use uv

EOF

git config commit.template .gitmessage
echo "✅ Setup commit message template"

# Create sync helper script
cat > "scripts/sync_upstream.sh" << 'EOF'
#!/bin/bash
# Helper script for syncing with upstream while protecting changes

set -e

echo "🔄 Syncing with upstream..."

# Validate current state
echo "Validating current migration state..."
uv run python scripts/validate_migration.py || {
    echo "❌ Current state validation failed. Fix issues before syncing."
    exit 1
}

# Create backup
BACKUP_BRANCH="pre-sync-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BACKUP_BRANCH"
git checkout -
echo "✅ Created backup branch: $BACKUP_BRANCH"

# Fetch upstream
git fetch upstream

# Show what would be merged
echo "📋 Changes to be merged:"
git log --oneline HEAD..upstream/main

read -p "Continue with merge? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Sync cancelled"
    exit 0
fi

# Perform merge
git merge upstream/main --no-ff || {
    echo "❌ Merge failed. Resolve conflicts and validate before committing."
    echo "Use: uv run python scripts/validate_migration.py"
    exit 1
}

echo "✅ Sync completed successfully"
EOF

chmod +x "scripts/sync_upstream.sh"
echo "✅ Created upstream sync helper"

# Create quick validation alias
cat >> ".bashrc" << 'EOF' || true

# DeepResearchAgent migration validation alias
alias validate-migration='uv run python scripts/validate_migration.py'
alias test-migration='uv run python scripts/test_migration.py'

EOF

echo "✅ Git protection setup complete!"
echo ""
echo "📋 Available commands:"
echo "  ./scripts/sync_upstream.sh    - Safely sync with upstream"
echo "  validate-migration           - Quick validation"
echo "  test-migration              - Full test suite"
echo ""
echo "🔧 Protected files configured in .gitattributes"
echo "🛡️ Pre-merge validation hook installed"
echo "📝 Commit message template configured"