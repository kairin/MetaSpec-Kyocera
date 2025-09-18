#!/bin/bash
# Complete Git Archive and Push Script
# Handles entire workflow: branch creation -> commit -> push -> merge

set -e

DESCRIPTION="$1"
COMMIT_MSG="$2"

if [ -z "$DESCRIPTION" ] || [ -z "$COMMIT_MSG" ]; then
    echo "❌ Usage: ./scripts/git_archive_push.sh 'brief-description' 'Detailed commit message'"
    echo "Example: ./scripts/git_archive_push.sh 'poetry-to-uv-migration' 'Complete migration from Poetry to uv with Python 3.13'"
    exit 1
fi

DATETIME=$(date +"%Y%m%d-%H%M%S")
BRANCH_NAME="archive/${DATETIME}-${DESCRIPTION}"

echo "🔄 Creating archive branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

echo "📝 Staging changes..."
git add .

echo "💾 Committing changes..."
git commit -m "${COMMIT_MSG}

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo "📤 Pushing archive branch..."
git push -u origin "$BRANCH_NAME"

echo "🔄 Merging to main..."
git checkout main
git merge "$BRANCH_NAME" --no-ff

echo "📤 Pushing main..."
git push origin main

echo "✅ Archive complete: $BRANCH_NAME"
echo "🎯 All changes preserved in archive branch and merged to main"