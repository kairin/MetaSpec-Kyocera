# Git Workflow & Branch Strategy

**Project**: Kyocera Meter Reading Management System  
**Version**: 1.0.0  
**Date**: 2025-09-11

## Core Principles

1. **Historical Preservation**: Every branch represents a point-in-time snapshot
2. **Never Delete**: Branches are permanent historical records
3. **Timestamp Precision**: Branch names include seconds for uniqueness
4. **Main Stability**: Main branch always contains stable, reviewed code
5. **Descriptive Naming**: Branch names clearly indicate purpose and time

## Branch Naming Convention

### Format
```
YYYY-MM-DD-HH-MM-SS-description
```

### Components
- **YYYY**: 4-digit year
- **MM**: 2-digit month (01-12)
- **DD**: 2-digit day (01-31)
- **HH**: 2-digit hour (00-23)
- **MM**: 2-digit minute (00-59)
- **SS**: 2-digit second (00-59) - REQUIRED for uniqueness
- **description**: Kebab-case feature/fix description

### Examples
```
2025-09-11-14-30-45-add-export-feature
2025-09-11-15-45-12-fix-email-parsing-bug
2025-09-11-16-20-00-update-documentation
```

## Workflow Steps

### 1. Create Feature Branch

```bash
# Automatic timestamp generation (RECOMMENDED)
git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-add-export-feature

# Manual (ensure correct format)
git checkout -b 2025-09-11-14-30-45-add-export-feature

# Using helper script
./scripts/create-new-feature.sh "add-export-feature"
```

### 2. Develop Feature

```bash
# Make changes following TDD
# 1. Write failing tests
uv run pytest tests/integration/test_new_feature.py  # Should fail

# 2. Implement feature
# Edit files...

# 3. Verify tests pass
uv run pytest tests/integration/test_new_feature.py  # Should pass

# 4. Run full test suite
uv run pytest
```

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add export feature for meter readings

- Implement CSV, Excel, and JSON export formats
- Add CLI command: meter-cli export
- Add API endpoint: /api/export
- Include comprehensive tests
- Update documentation

Tested with 100+ meter readings across different formats"
```

### 4. Push to Remote

```bash
# Push branch to remote (preserves timestamp in branch name)
git push -u origin $(git branch --show-current)

# Or explicitly
git push -u origin 2025-09-11-14-30-45-add-export-feature
```

### 5. Create Pull Request

```bash
# Using GitHub CLI (recommended)
gh pr create \
  --title "Add export feature for meter readings" \
  --body "## Summary
- Implements multiple export formats (CSV, Excel, JSON)
- Adds new CLI commands for export operations
- Includes API endpoints for web dashboard integration

## Test Coverage
- Contract tests: 100%
- Integration tests: 95%
- Unit tests: 90%

## Documentation
- Updated CLAUDE.md with new commands
- Added examples to quickstart.md
- API documentation updated

## Performance
- Exports 1000 readings in <2 seconds
- Memory usage optimized for large datasets" \
  --base main

# Or use web interface
# Navigate to: https://github.com/your-org/repo/pull/new/2025-09-11-14-30-45-add-export-feature
```

### 6. Code Review Process

```bash
# Request reviewers
gh pr edit --add-reviewer @teammate1,@teammate2

# Address review comments
git add .
git commit -m "Address review comments: improve error handling"
git push

# After approval, DO NOT squash commits
# Preserve full history for traceability
```

### 7. Merge to Main

```bash
# Merge PR (preserves branch)
gh pr merge --merge  # Use merge commit (NOT squash)

# Or from web UI
# Select "Create a merge commit" option
# DO NOT select "Squash and merge"
# DO NOT delete branch after merge
```

### 8. Post-Merge

```bash
# Switch back to main
git checkout main
git pull origin main

# Create new branch for next feature
git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-next-feature

# Branch remains in remote for historical reference
# Can be checked out anytime:
git checkout 2025-09-11-14-30-45-add-export-feature
```

## Branch Management

### Viewing Branches

```bash
# List all branches with timestamps
git branch -a | sort

# Filter by date
git branch -a | grep "2025-09-11"

# Show branch creation info
git for-each-ref --format='%(refname:short) %(committerdate:iso)' refs/heads/ | sort -k2
```

### Checking Out Historical Branches

```bash
# Checkout specific point in time
git checkout 2025-09-11-14-30-45-add-export-feature

# Create new branch from historical point
git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-bugfix-from-old 2025-09-11-14-30-45-add-export-feature
```

### Branch Protection Rules

Configure in GitHub/GitLab:

1. **Main Branch Protection**:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date
   - Include administrators

2. **Historical Branch Protection**:
   - Protect branches matching pattern: `20*-*`
   - Prevent deletion
   - Prevent force pushes

## Commit Message Standards

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Build process or auxiliary tool changes

### Example
```
feat: Add export functionality for meter readings

- Implement CSV export with customizable columns
- Add Excel export with formatting and charts
- Include JSON export for API integration
- Support batch export for multiple devices

Tests added for all export formats
Performance: Exports 1000 records in <2 seconds

Closes #123
```

## Emergency Procedures

### Reverting Changes

```bash
# Create revert branch with timestamp
git checkout main
git pull origin main
git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-revert-export-feature

# Revert the merge commit
git revert -m 1 <merge-commit-hash>

# Push and create PR
git push -u origin $(git branch --show-current)
gh pr create --title "Revert: Export feature causing issues" --body "Reverting due to production issue #456"
```

### Hotfix Process

```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-hotfix-critical-bug

# Make minimal fix
# ... edit files ...

# Fast-track through review
git add .
git commit -m "hotfix: Critical bug in email processing"
git push -u origin $(git branch --show-current)

# Create urgent PR
gh pr create --title "HOTFIX: Critical email processing bug" --label "urgent"
```

## Git Configuration

### Recommended Settings

```bash
# Set up UV as default for Python projects
git config --global alias.uv-install '!uv pip install -r requirements.txt'
git config --global alias.uv-sync '!uv pip sync requirements.txt'

# Helpful aliases for timestamped branches
git config --global alias.new-branch '!git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-'
git config --global alias.branch-time '!git for-each-ref --format="%(refname:short) %(committerdate:iso)" refs/heads/ | sort -k2'

# Prevent accidental branch deletion
git config --global receive.denyDeletes true
git config --global receive.denyNonFastForwards true
```

### Pre-commit Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Run tests before commit
uv run pytest tests/contract/ || exit 1

# Check code formatting
uv run black --check src/ || exit 1

# Verify UV is being used (no pip)
if grep -r "pip install" --include="*.md" --include="*.py" .; then
  echo "ERROR: Found 'pip install' - use 'uv pip install' instead"
  exit 1
fi
```

## Best Practices

1. **Always use timestamps**: Never create branches without full timestamp
2. **Never force push**: Preserve all history
3. **Never delete branches**: They're historical records
4. **Use descriptive names**: Branch name should clearly indicate purpose
5. **Test before pushing**: Run full test suite locally
6. **Document changes**: Update CLAUDE.md and relevant docs
7. **Small, focused PRs**: One feature/fix per PR
8. **Review thoroughly**: All code must be reviewed before merge
9. **Keep main stable**: Only merge tested, reviewed code
10. **Use UV exclusively**: No direct pip commands ever

## Troubleshooting

### Branch Name Conflicts

```bash
# If branch already exists (rare with seconds precision)
git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-feature-v2
```

### Finding Lost Work

```bash
# Search all branches for specific changes
git branch -a | xargs -I {} git log {} --grep="specific change"

# Find branches modified on specific date
git for-each-ref --format='%(refname:short) %(committerdate:short)' refs/heads/ | grep "2025-09-11"
```

### Syncing with Main

```bash
# Update feature branch with latest main
git checkout main
git pull origin main
git checkout 2025-09-11-14-30-45-my-feature
git merge main

# Resolve conflicts if any
git add .
git commit -m "Merge main into feature branch"
git push
```

## Automation Scripts

### create-new-feature.sh
```bash
#!/bin/bash
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
DESCRIPTION=$1

if [ -z "$DESCRIPTION" ]; then
  echo "Usage: ./create-new-feature.sh <description>"
  exit 1
fi

BRANCH_NAME="${TIMESTAMP}-${DESCRIPTION}"
git checkout -b "$BRANCH_NAME"
echo "Created branch: $BRANCH_NAME"
```

### list-branches-by-date.sh
```bash
#!/bin/bash
git for-each-ref --sort=-committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short) %(subject)' \
  | head -20
```

---

*This workflow ensures complete traceability and historical preservation of all development work.*