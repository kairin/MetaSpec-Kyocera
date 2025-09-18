# MetaSpec-Kyocera System - LLM Instructions

> 🔧 **CRITICAL**: This file contains NON-NEGOTIABLE requirements that ALL AI assistants (Claude, Gemini, ChatGPT, etc.) working on this repository MUST follow at ALL times.

## 🎯 Project Overview

**MetaSpec-Kyocera System** is a unified architecture combining DeepResearchAgent, claude-guardian-agents, spec-kit, and MonthlyKyocera for complete Kyocera billing management with zero additional costs.

**Quick Links:** [Planning](PLANNING.md) • [Phase 1](PHASE_1_FOUNDATION.md) • [Web Integration](WEB_INTERFACE_INTEGRATION.md) • [Architecture](docs/ARCHITECTURE.md)

## ⚡ NON-NEGOTIABLE REQUIREMENTS

### 🚨 CRITICAL: Zero-Cost Operations
- **NO CLOUD SERVICES**: All processing runs locally only
- **NO SUBSCRIPTION FEES**: No external services that incur charges
- **NO GITHUB ACTIONS**: Use local runners only to avoid GitHub Actions charges
- **LOCAL CI/CD**: All automation via cron/systemd locally

### 🚨 CRITICAL: Package Management
- **UV EXCLUSIVELY**: NEVER use pip, conda, poetry, or any other Python package manager
- **Python 3.13+**: Ubuntu 25.04 built-in version only
- **Commands**: All Python operations through `uv run`, `uv add`, `uv sync`

### 🚨 CRITICAL: Web Interface (NON-NEGOTIABLE)
- **Framework**: Astro.build ONLY for web interface
- **Styling**: TailwindCSS ONLY for CSS framework
- **Components**: shadcn/ui ONLY for UI component library
- **NO ALTERNATIVES**: These choices are non-negotiable

### 🚨 CRITICAL: Data Storage
- **Database**: DuckDB ONLY for all data storage and archiving
- **File Format**: DuckDB files with compression for email archives
- **NO ALTERNATIVES**: No PostgreSQL, MySQL, SQLite, or cloud databases

### 🚨 CRITICAL: Branch Management & Git Strategy

#### Branch Preservation (MANDATORY)
- **NEVER DELETE BRANCHES** without explicit user permission
- **ALL BRANCHES** contain valuable historical information
- **NO** automatic cleanup with `git branch -d`
- **YES** to automatic merge to main branch, preserving dedicated branch

#### Branch Naming (MANDATORY SCHEMA)
**Format**: `YYYYMMDD-HHMMSS-type-short-description`

Examples:
- `20250919-143000-feat-astro-dashboard`
- `20250919-143515-fix-duckdb-connection`
- `20250919-144030-docs-api-endpoint-updates`

#### GitHub Safety Strategy
```bash
# MANDATORY: Every commit must use this workflow
DATETIME=$(date +"%Y%m%d-%H%M%S")
BRANCH_NAME="${DATETIME}-feat-description"
git checkout -b "$BRANCH_NAME"
git add .
git commit -m "Descriptive commit message

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>"
git push -u origin "$BRANCH_NAME"
git checkout main
git merge "$BRANCH_NAME" --no-ff
git push origin main
# NEVER: git branch -d "$BRANCH_NAME"
```

## 🏗️ System Architecture

### Directory Structure (MANDATORY)
```
/home/kkk/Apps/MetaSpec-Kyocera/
├── core/                   # DeepResearchAgent foundation
│   ├── agents/            # Guardian agents (52 total)
│   ├── models/            # Multi-provider model support
│   └── orchestration/     # Central coordination
├── specs/                  # spec-kit integration
│   ├── workflows/         # Standardized processes
│   ├── templates/         # Reusable specifications
│   └── kyocera/          # Domain-specific specs
├── domains/               # Domain implementations
│   ├── kyocera/          # Enhanced MonthlyKyocera
│   ├── billing/          # Billing management
│   └── archival/         # DuckDB data management
├── data/                  # Zero-cost data layer
│   ├── duckdb/           # Primary database files
│   ├── archives/         # Compressed email archives
│   └── web-dist/         # Built Astro site
├── web/                   # Astro web interface (NON-NEGOTIABLE)
│   ├── src/
│   │   ├── components/   # shadcn/ui components
│   │   ├── pages/        # Astro pages
│   │   └── layouts/      # Page layouts
│   ├── public/           # Static assets
│   └── astro.config.mjs  # Astro configuration
├── local-infra/          # Zero-cost infrastructure
│   ├── runners/          # Local CI/CD scripts
│   ├── monitoring/       # Log aggregation
│   └── backup/           # Archive strategies
└── docs/                 # Auto-generated Astro documentation
```

### Technology Stack (NON-NEGOTIABLE)

**Backend (Python)**:
- **Python**: 3.13+ (Ubuntu 25.04 built-in)
- **Package Manager**: uv EXCLUSIVELY
- **Database**: DuckDB for all data storage
- **API**: FastAPI for web interface backend
- **Orchestration**: DeepResearchAgent async framework

**Frontend (Web Interface)**:
- **Framework**: Astro.build (Static Site Generation + SSR)
- **Styling**: TailwindCSS (utility-first CSS)
- **Components**: shadcn/ui (accessible component library)
- **Charts**: Recharts for data visualization
- **Build**: Vite-based (built into Astro)

## 📊 Core Functionality

### Primary Goals
1. **Daily Meter Reading Collection**: Automated email processing and data extraction
2. **Monthly Invoice Reconciliation**: Match bills to actual device usage
3. **3-Year Cost Projections**: Generate accurate PO estimates
4. **Complete Audit Trail**: All emails archived with reconstruction capability

### Agent Orchestration (52 Agents)
```
Meta-Orchestrator Layer:
├── 001-kyocera-strategic-guardian     # Business logic & planning
├── 002-spec-workflow-guardian         # spec-kit integration
└── 003-data-archival-guardian         # DuckDB management

Specialized Execution Layer:
├── 021-email-processing-guardian      # Email handling
├── 022-meter-extraction-guardian      # Device data extraction
├── 023-billing-calculation-guardian   # Cost projections
├── 024-invoice-tracking-guardian      # E-invoice management
└── 025-reporting-guardian             # Reports and dashboards
```

## 🛠️ Development Commands (MANDATORY)

### Environment Setup
```bash
# MANDATORY: Use uv exclusively
cd /home/kkk/Apps/MetaSpec-Kyocera
uv venv --python 3.13
source .venv/bin/activate
uv sync

# Install web dependencies
cd web/
npm install
```

### Daily Development Workflow
```bash
# Backend Development
source .venv/bin/activate
uv run python domains/kyocera/web_api.py  # Start FastAPI :8000

# Frontend Development
cd web/
npm run dev    # Start Astro dev server :3000
npm run build  # Build static assets

# Testing
uv run pytest tests/
cd web/ && npm run test
```

### Database Operations
```bash
# Initialize database
uv run python data/init_database.py

# Backup database
uv run python local-infra/backup/backup_manager.py

# Validate data integrity
uv run python domains/kyocera/data_validator.py
```

## 🔄 GitHub Pages & Documentation

### Zero-Cost GitHub Pages Setup
```yaml
# .github/workflows/pages.yml (SAFE - uses GitHub's free tier)
name: Deploy Astro to GitHub Pages
on:
  push:
    branches: [main]
    paths: ['docs/**', 'web/**']
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - name: Install dependencies
        run: cd web && npm ci
      - name: Build Astro site
        run: |
          cd web
          npm run build
          cp -r dist/* ../docs/
      - uses: actions/upload-pages-artifact@v2
        with:
          path: ./docs

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/deploy-pages@v3
        id: deployment
```

### Local Documentation Builder
```bash
# File: local-infra/runners/build-docs.sh
#!/bin/bash
set -e

echo "🏗️ Building documentation site..."

# Build Astro site with documentation
cd web/
npm run build

# Copy built site to docs for GitHub Pages
cp -r dist/* ../docs/

# Copy markdown files as Astro pages
cp ../PLANNING.md src/pages/planning.md
cp ../PHASE_1_FOUNDATION.md src/pages/phase-1.md
cp ../WEB_INTERFACE_INTEGRATION.md src/pages/web-integration.md

echo "✅ Documentation site built and ready for GitHub Pages"
```

## 🚨 LLM Conversation Logging (MANDATORY)

**CRITICAL REQUIREMENT**: All AI assistants working on this repository **MUST** save complete conversation logs.

### Requirements
- **Complete Logs**: Save entire conversation from start to finish
- **Exclude Sensitive Data**: Remove API keys, passwords, personal information
- **Storage Location**: `docs/development/conversation_logs/`
- **Naming Convention**: `CONVERSATION_LOG_YYYYMMDD_DESCRIPTION.md`

### Example
```bash
# After completing work, save conversation log:
cp /path/to/conversation.md docs/development/conversation_logs/CONVERSATION_LOG_20250919_phase1_implementation.md
git add docs/development/conversation_logs/
git commit -m "Add conversation log for Phase 1 implementation"
```

## ⚠️ ABSOLUTE PROHIBITIONS

### DO NOT
- Use any package manager except uv for Python
- Use cloud services that incur charges
- Delete branches without explicit permission
- Use GitHub Actions for anything that consumes minutes
- Change web interface technology choices (Astro/TailwindCSS/shadcn)
- Commit sensitive data (API keys, passwords)
- Use databases other than DuckDB

### DO NOT BYPASS
- Branch preservation requirements
- Zero-cost operation constraints
- Web interface technology requirements
- uv-only package management
- Conversation logging requirements

## ✅ MANDATORY ACTIONS

### Before Every Commit
1. **Branch Creation**: Use timestamp-based branch naming
2. **Testing**: Run `uv run pytest tests/` and `cd web/ && npm run test`
3. **Build Validation**: Ensure `cd web/ && npm run build` succeeds
4. **Documentation**: Update relevant docs if adding features
5. **Conversation Log**: Save complete AI conversation log

### Quality Gates
- All tests pass without errors
- Astro site builds successfully
- DuckDB operations complete without corruption
- Email reconstruction capability verified
- Branch preservation maintained

## 🎯 Success Criteria

### Operational Metrics
- **Email Processing**: 100% success rate for valid emails
- **Web Interface**: Sub-2 second page load times
- **Data Accuracy**: <1% variance between readings and invoices
- **Cost Prediction**: ±5% accuracy for quarterly projections

### Technical Metrics
- **Zero Cost**: No external service charges incurred
- **Data Integrity**: 100% email reconstruction capability
- **Uptime**: >99% availability during business hours
- **Storage Efficiency**: >80% compression ratio for archived emails

## 📚 Documentation & Help

### Key Documents
- [PLANNING.md](PLANNING.md) - Comprehensive system planning
- [PHASE_1_FOUNDATION.md](PHASE_1_FOUNDATION.md) - Implementation guide
- [WEB_INTERFACE_INTEGRATION.md](WEB_INTERFACE_INTEGRATION.md) - Web interface details

### Support Commands
```bash
# Get help
uv run python -m src.help
cd web/ && npm run help

# Validate system
uv run python scripts/validate_system.py

# Emergency recovery
uv run python tools/emergency/system_recovery.py
```

### GitHub Pages URL
- **Production**: `https://kairin.github.io/MetaSpec-Kyocera/`
- **Staging**: Built from branches automatically

## 🔄 Continuous Integration (Local)

### Daily Automation (Cron)
```bash
# File: local-infra/runners/daily-ci.sh
#!/bin/bash
# Add to crontab: 0 9,13,17 * * * /path/to/daily-ci.sh

source .venv/bin/activate

# Process emails
uv run python domains/kyocera/email_processor.py

# Update documentation site
cd web/
npm run build
cp -r dist/* ../docs/

# Commit and push updates
DATETIME=$(date +"%Y%m%d-%H%M%S")
git checkout -b "${DATETIME}-auto-daily-update"
git add docs/
git commit -m "Daily documentation update

🤖 Automated daily build
Co-Authored-By: System <system@metaspec-kyocera>"
git push -u origin "${DATETIME}-auto-daily-update"
git checkout main
git merge "${DATETIME}-auto-daily-update" --no-ff
git push origin main
```

---

**CRITICAL**: These requirements are NON-NEGOTIABLE. All AI assistants must follow these guidelines exactly. Failure to comply may result in system corruption, additional costs, or data loss.

**Version**: 1.0
**Last Updated**: 2025-09-19
**Status**: ACTIVE - MANDATORY COMPLIANCE
**Review**: Required before any major changes