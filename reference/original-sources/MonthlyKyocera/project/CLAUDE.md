# CLAUDE.md - Project Context for Claude Code

## Project Overview
**Name**: Kyocera Meter Reading Management System
**Type**: Python CLI batch processing tool
**Purpose**: Automate processing of monthly meter readings from Kyocera office devices received via email

## Technology Stack

### Backend (Python)
- **Language**: Python 3.11+
- **Package Manager**: UV (Astral) EXCLUSIVELY - No pip commands allowed
- **Virtual Environment**: Managed by UV only
- **TUI Framework**: Textual or Rich
- **CLI Framework**: Built-in argparse
- **Database**: DuckDB for archive and long-term storage
- **PDF Generation**: fpdf2
- **Email Parsing**: email (standard library) - No file size limits
- **Email Compression**: zstd/gzip for archives <10MB
- **File Operations**: pathlib (standard library)
- **Backup Formats**: Markdown (MD) and YAML
- **API Framework**: FastAPI with Uvicorn
- **Testing**: pytest
- **Logging**: JSON structured logging

### Web Dashboard (Astro)
- **Framework**: Astro (static site generator)
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Charts**: Recharts or Chart.js for usage analytics
- **Data Fetching**: DuckDB WASM or API endpoints
- **Features**:
  - Device usage trends over time
  - Monthly/yearly comparisons
  - Export reports for departments
  - Full meter reading details
  - Search and filter capabilities

## Project Structure
```
src/
├── models/
│   └── meter_reading.py      # Data models
├── services/
│   ├── email_parser.py        # .eml file parsing
│   ├── device_extractor.py    # Pattern matching
│   ├── pdf_converter.py       # PDF generation
│   ├── folder_manager.py      # Directory operations
│   └── archive_manager.py     # DuckDB archive operations
├── tui/
│   └── meter_tui.py          # Terminal UI interface
├── cli/
│   └── meter_cli.py          # CLI interface
├── api/
│   └── meter_api.py          # REST API for web dashboard
└── lib/
    └── meter_processor.py     # Main orchestration

web/                          # Astro web dashboard
├── src/
│   ├── components/           # Reusable components
│   │   ├── ui/              # shadcn/ui components
│   │   └── charts/          # Data visualization
│   ├── pages/               # Astro pages
│   │   ├── index.astro      # Dashboard home
│   │   ├── devices/         # Device details
│   │   └── reports/         # Report generation
│   └── layouts/             # Page layouts
├── public/                  # Static assets
└── astro.config.mjs         # Astro configuration

tests/
├── contract/                # API contract tests
├── integration/             # Service integration tests
└── unit/                    # Unit tests

devices/                     # Processed meter readings
├── <MODEL>/
│   └── <SERIAL>/
│       └── <YYYY-MM-DD>/
│           ├── *.pdf
│           ├── *.txt
│           ├── *.md         # Markdown backup
│           └── *.yaml       # YAML backup

emails/                      # Email processing (original files preserved)
├── pending/                 # To be processed
├── processed/              # Successfully processed
├── quarantine/             # Failed processing
└── archive/                 # Long-term storage

database/
└── meter_readings.duckdb   # Archive database
```

## Critical Requirements

### UV Package Manager (MANDATORY)
- **NEVER use pip directly** - All Python operations through UV
- **Virtual environments**: `uv venv` only
- **Install packages**: `uv pip install` only
- **Freeze requirements**: `uv pip freeze` only
- **Sync environments**: `uv pip sync` only

### Email Processing
- **No file size limits** on input .eml files
- **Compression target**: <10MB for archive storage
- **Email reconstruction**: Full .eml file recovery capability
- **Thread preservation**: Complete conversation tracking

### Git Branch Strategy
- **Format**: `YYYY-MM-DD-HH-MM-SS-description`
- **Timestamp**: System clock at commit time (seconds precision!)
- **Description**: From commit message (kebab-case)
- **NEVER delete branches** - Historical preservation
- **Main branch**: Default, all PRs merge here

## Development Setup
```bash
# Install UV package manager (REQUIRED)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment with UV (NO pip venv!)
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies (UV ONLY)
uv pip install -r requirements.txt

# Install dev dependencies (UV ONLY)
uv pip install -r requirements-dev.txt
```

## Key Commands
```bash
# Process emails
uv run meter-cli process [--input=./emails/pending] [--dry-run]

# Launch Terminal UI
uv run python -m src.tui.meter_tui

# Start API server
uv run uvicorn src.api.meter_api:app --reload

# Validate structure
uv run meter-cli validate [--repair]

# Generate reports
uv run meter-cli report [--start-date=YYYY-MM-DD] [--end-date=YYYY-MM-DD]

# List devices
uv run meter-cli list [--type=devices|readings]

# Debug single email
uv run meter-cli parse <file.eml>

# Run tests
uv run pytest tests/
uv run pytest tests/contract/ -v     # Contract tests first
uv run pytest tests/integration/ -v  # Then integration
uv run pytest tests/unit/ -v         # Finally unit tests
```

## Development Workflow
1. **TDD Approach**: Write tests first (RED-GREEN-Refactor)
2. **Test Order**: Contract → Integration → Unit
3. **File Naming**: `{date}_{model}_{serial}_{timestamp}_meter_reading.{ext}`
4. **Error Handling**: Quarantine failed emails, comprehensive logging

## Key Patterns
- **Device Identification**: Extract serial/model from email subject, body, filename
- **Folder Structure**: `devices/<MODEL>/<SERIAL>/<YYYY-MM-DD>/`
- **Duplicate Handling**: Append `_1`, `_2` to filenames
- **Date Extraction**: Try multiple sources (subject, body, received date)

## Configuration
```python
# Default settings
INPUT_DIR = "./emails/pending"
OUTPUT_DIR = "./devices"
LOG_LEVEL = "INFO"
RETENTION_MONTHS = 24
BATCH_SIZE = 50
```

## Testing Approach
```python
# Contract test example
def test_email_parser_contract():
    """Parser must return expected schema"""
    result = EmailParser.parse_email("test.eml")
    assert "received_date" in result
    assert "subject" in result
    assert "body_text" in result

# Integration test example
def test_process_email_flow():
    """Full processing flow must work"""
    result = MeterProcessor.process_email("sample.eml")
    assert Path(result["pdf_path"]).exists()
    assert Path(result["txt_path"]).exists()
```

## Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| Missing device serial | Check quarantine folder, manual review |
| Duplicate readings | System auto-appends sequence numbers |
| Corrupted .eml file | Re-export from email client |
| Folder permission error | Run `validate --repair` with proper permissions |

## Performance Targets
- Process 100 emails/minute
- Single email < 3 seconds
- PDF generation < 1 second
- Support 50+ devices

## Security Considerations
- Sanitize filenames (prevent path traversal)
- Remove PII from logs
- Quarantine suspicious files
- Read-only after processing

## Git Workflow & Branch Strategy
- **Branch Naming**: `YYYY-MM-DD-HH-MM-SS-description` (seconds required!)
- **Creation**: `git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-feature-name`
- **Default Branch**: main (preserved)
- **History Preservation**: Each branch maintains point-in-time state
- **Commit Strategy**: Descriptive messages with timestamp branches
- **Never Delete**: Historical branches preserve all versions
- **PR Process**: Create PR → Review → Merge to main → Keep branch

## Recent Changes
- 2025-09-09: Initial project setup and planning
- 2025-09-09: Created data model and service contracts
- 2025-09-09: Defined CLI interface and quickstart guide
- 2025-09-11: Added DuckDB, TUI, backup formats, git branch strategy

## Next Steps
1. Implement contract tests (failing)
2. Create service implementations
3. Build CLI interface
4. Add integration tests
5. Performance optimization

---
*This file is maintained for AI assistant context. Keep under 150 lines.*