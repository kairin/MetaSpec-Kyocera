#!/bin/bash
# Git Archive Helper Script
# Creates archive branch with datetime naming

set -e

DESCRIPTION="$1"
if [ -z "$DESCRIPTION" ]; then
    echo "❌ Usage: ./scripts/git_archive.sh 'brief-description'"
    echo "Example: ./scripts/git_archive.sh 'fix-circular-imports'"
    exit 1
fi

DATETIME=$(date +"%Y%m%d-%H%M%S")
BRANCH_NAME="archive/${DATETIME}-${DESCRIPTION}"

echo "🔄 Creating archive branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

echo "✅ Archive branch created: $BRANCH_NAME"
echo "Next steps:"
echo "1. git add . && git commit -m 'Your commit message'"
echo "2. git push -u origin '$BRANCH_NAME'"
echo "3. git checkout main && git merge '$BRANCH_NAME' --no-ff"
echo "4. git push origin main"