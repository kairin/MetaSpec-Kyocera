# MetaSpec-Kyocera System

> **Unified Kyocera billing management system with zero additional costs**

A comprehensive architecture combining DeepResearchAgent, claude-guardian-agents, spec-kit, and MonthlyKyocera for complete daily meter reading collection, monthly invoice reconciliation, and 3-year cost projections.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd MetaSpec-Kyocera

# Setup Python environment (uv ONLY)
uv venv --python 3.13
source .venv/bin/activate
uv sync

# Setup web interface
cd web/
npm install
npm run dev  # Start development server

# Initialize database
cd ..
uv run python data/init_database.py
```

## 📋 Key Features

- **Daily Automation**: Automated email processing and meter reading extraction
- **Web Dashboard**: Modern Astro.build interface with TailwindCSS and shadcn/ui
- **Cost Projections**: 3-year forecasting for accurate PO planning
- **Zero Cost**: 100% local processing with GitHub Pages hosting
- **Complete Audit**: Email archival with reconstruction capability

## 🏗️ Architecture

- **Backend**: Python 3.13 + FastAPI + DuckDB
- **Frontend**: Astro.build + TailwindCSS + shadcn/ui
- **Orchestration**: 52 Guardian Agents + DeepResearchAgent
- **Workflows**: spec-kit driven development

## 📚 Documentation

| Category | Description | Location |
|----------|-------------|----------|
| **LLM Instructions** | Critical requirements for AI assistants | [AGENTS.md](AGENTS.md) |
| **Planning** | System architecture and implementation strategy | [docs/planning/](docs/planning/) |
| **Implementation** | Phase-by-phase development guides | [docs/implementation/](docs/implementation/) |
| **User Guides** | End-user documentation and tutorials | [docs/user-guides/](docs/user-guides/) |
| **API Reference** | Technical API documentation | [docs/api/](docs/api/) |
| **Development** | Developer setup and guidelines | [docs/development/](docs/development/) |

## ⚡ Non-Negotiable Requirements

1. **Zero Cost**: No cloud services or subscription fees
2. **uv Only**: Exclusive Python package management
3. **Web Stack**: Astro.build + TailwindCSS + shadcn/ui (no alternatives)
4. **DuckDB**: All data storage and archival
5. **Branch Preservation**: Never delete git branches

## 🔗 Quick Links

- **[System Planning](docs/planning/SYSTEM_PLANNING.md)** - Comprehensive planning document
- **[Phase 1 Guide](docs/implementation/PHASE_1_FOUNDATION.md)** - Implementation details
- **[Web Interface](docs/architecture/WEB_INTERFACE_INTEGRATION.md)** - Frontend architecture
- **[Development Setup](docs/development/DEVELOPMENT_SETUP.md)** - Getting started guide
- **[API Documentation](docs/api/API_REFERENCE.md)** - Backend API reference

## 🎯 Goals

1. **Daily Operations**: Collect meter readings from emails automatically
2. **Monthly Processing**: Reconcile invoices with actual device usage
3. **Yearly Planning**: Generate accurate 3-year cost projections for PO planning
4. **Compliance**: Track all e-invoices and maintain complete audit trail

## 🛠️ Technology Stack

- **Python**: 3.13+ with uv package management
- **Database**: DuckDB with compression and archival
- **Web Framework**: Astro.build for static site generation
- **Styling**: TailwindCSS utility-first framework
- **Components**: shadcn/ui accessible component library
- **API**: FastAPI for backend services
- **Orchestration**: Guardian Agents + DeepResearchAgent

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Status**: Active Development (Phase 1)
**Version**: 1.0.0
**Last Updated**: 2025-09-19