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
