# Quickstart Guide

**System**: Kyocera Meter Reading Management System  
**Version**: 1.0.0  
**Prerequisites**: Python 3.11+, UV package manager

## Installation

### 1. Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 2. Clone Repository

```bash
git clone https://github.com/your-org/kyocera-meter-reader.git
cd kyocera-meter-reader
```

### 3. Create Virtual Environment

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### 4. Install Dependencies

```bash
# Install production dependencies
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -r requirements-dev.txt
```

### 5. Initialize Database

```bash
# Create database directory
mkdir -p database

# Initialize DuckDB schema
python -c "
import duckdb
conn = duckdb.connect('database/meter_readings.duckdb')
with open('specs/002-claude-md-project/contracts/schema.sql', 'r') as f:
    conn.execute(f.read())
conn.close()
print('Database initialized successfully!')
"
```

### 6. Setup Directory Structure

```bash
# Create required directories
mkdir -p emails/pending emails/processed emails/quarantine emails/archive
mkdir -p devices
mkdir -p reports
mkdir -p logs

# Set permissions
chmod 755 emails devices reports logs
```

## Basic Usage

### Processing Emails (CLI)

```bash
# Process all pending emails
uv run meter-cli process

# Process with dry run (no changes)
uv run meter-cli process --dry-run

# Process specific batch size
uv run meter-cli process --batch-size 10

# Process single email for debugging
uv run meter-cli parse emails/pending/sample.eml
```

### Terminal User Interface (TUI)

```bash
# Launch interactive TUI
uv run python -m src.tui.meter_tui

# TUI Commands:
# - Arrow keys: Navigate
# - Enter: Select
# - q: Quit
# - r: Refresh
# - f: Filter devices
# - s: Search
```

### Web Dashboard

```bash
# Start API server
uv run uvicorn src.api.meter_api:app --reload --port 8000

# Access dashboard at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Managing Devices

```bash
# List all devices
uv run meter-cli list --type=devices

# Show device details
uv run meter-cli device --serial ABC1234567

# Update device location
uv run meter-cli device --serial ABC1234567 --location "Building B, Floor 3"

# Deactivate device
uv run meter-cli device --serial ABC1234567 --status inactive
```

### Generating Reports

```bash
# Generate monthly report for current month
uv run meter-cli report --type monthly

# Generate device-specific report
uv run meter-cli report --type device --serial ABC1234567 --format pdf

# Generate yearly summary
uv run meter-cli report --type yearly --year 2024 --format excel

# Generate department report
uv run meter-cli report --type department --location "Building A" --format csv
```

### Data Validation

```bash
# Validate folder structure
uv run meter-cli validate

# Auto-repair folder issues
uv run meter-cli validate --repair

# Check for duplicate readings
uv run meter-cli validate --check-duplicates

# Verify database integrity
uv run meter-cli validate --check-database
```

## Testing

### Run All Tests

```bash
# Run complete test suite
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

### Run Tests by Type

```bash
# Contract tests first (API contracts)
uv run pytest tests/contract/ -v

# Integration tests (service interactions)
uv run pytest tests/integration/ -v

# Unit tests (individual components)
uv run pytest tests/unit/ -v

# Specific test file
uv run pytest tests/integration/test_email_processing.py -v
```

### Test Email Processing

```bash
# Create test email
cat > emails/pending/test.eml << 'EOF'
From: printer@office.local
To: admin@company.com
Subject: Meter Reading - TASKalfa 3253ci - ABC1234567
Date: Mon, 11 Sep 2025 10:00:00 +0000

Device: TASKalfa 3253ci
Serial Number: ABC1234567
Reading Date: 2025-09-11

Counters:
Total: 150000
Black: 120000
Color: 30000
Scan: 5000
Fax: 200
EOF

# Process test email
uv run meter-cli process --input emails/pending/test.eml

# Verify output
ls -la devices/TASKalfa_3253ci/ABC1234567/2025-09-11/
```

## Common Operations

### Monitor Processing

```bash
# View processing logs
uv run meter-cli logs --tail 50

# Monitor in real-time
uv run meter-cli logs --follow

# Filter by status
uv run meter-cli logs --status failed --last 24h

# Export logs
uv run meter-cli logs --export logs/processing_$(date +%Y%m%d).json
```

### Database Operations

```bash
# Backup database
cp database/meter_readings.duckdb database/backup_$(date +%Y%m%d).duckdb

# Query database directly
uv run python -c "
import duckdb
conn = duckdb.connect('database/meter_readings.duckdb', read_only=True)
result = conn.execute('SELECT COUNT(*) FROM meter_readings').fetchone()
print(f'Total readings: {result[0]}')
"

# Export data to CSV
uv run meter-cli export --format csv --output exports/readings.csv

# Archive old data
uv run meter-cli archive --older-than 24months
```

### Troubleshooting

```bash
# Check system health
uv run meter-cli health

# Diagnose email processing issues
uv run meter-cli diagnose emails/quarantine/failed.eml

# Reset processing queue
uv run meter-cli reset-queue

# Clean temporary files
uv run meter-cli clean --temp-files

# Rebuild search index
uv run meter-cli rebuild-index
```

## API Examples

### Process Emails via API

```bash
# Trigger email processing
curl -X POST http://localhost:8000/api/emails/process \
  -H "Content-Type: application/json" \
  -d '{"batch_size": 50, "dry_run": false}'
```

### Get Device List

```bash
# List all active devices
curl http://localhost:8000/api/devices?status=active

# Get specific device
curl http://localhost:8000/api/devices/ABC1234567
```

### Get Meter Readings

```bash
# Get readings for specific device
curl http://localhost:8000/api/devices/ABC1234567/readings

# Get readings for date range
curl "http://localhost:8000/api/devices/ABC1234567/readings?start_date=2025-09-01&end_date=2025-09-30"
```

### Generate Report

```bash
# Generate monthly report
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "monthly",
    "start_date": "2025-09-01",
    "end_date": "2025-09-30",
    "format": "pdf"
  }'
```

### Dashboard Statistics

```bash
# Get dashboard stats
curl http://localhost:8000/api/dashboard/stats

# Get usage trends
curl http://localhost:8000/api/dashboard/trends?period=monthly&months=12
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# Application settings
APP_ENV=development
LOG_LEVEL=INFO
DEBUG=false

# Database
DATABASE_PATH=database/meter_readings.duckdb
DATABASE_BACKUP_PATH=database/backups

# Email processing
EMAIL_INPUT_DIR=emails/pending
EMAIL_PROCESSED_DIR=emails/processed
EMAIL_QUARANTINE_DIR=emails/quarantine
EMAIL_BATCH_SIZE=50

# File paths
DEVICE_OUTPUT_DIR=devices
REPORT_OUTPUT_DIR=reports
LOG_DIR=logs

# Performance
MAX_WORKERS=4
PROCESSING_TIMEOUT=300

# Data retention
RETENTION_MONTHS=24
LOG_RETENTION_DAYS=90

# API settings
API_HOST=0.0.0.0
API_PORT=8000
API_KEY=your-secure-api-key

# Web dashboard
DASHBOARD_URL=http://localhost:3000
```

## Email Reconstruction & Compression

### Compress Large Emails

```bash
# Compress emails via CLI
uv run meter-cli compress-email --message-id "<msg-id>" --method zstd

# Batch compress old emails
uv run meter-cli compress --older-than 90days --target-size 10mb

# Check compression stats
uv run meter-cli stats compression
```

### Reconstruct Original Emails

```bash
# Reconstruct single email
uv run meter-cli reconstruct --message-id "<msg-id>" --output recovered.eml

# Reconstruct email thread
uv run meter-cli reconstruct-thread --thread-id "<thread-id>" --output thread/

# Verify reconstruction
uv run meter-cli verify-reconstruction --input recovered.eml
```

### Thread Management

```bash
# View email threads
uv run meter-cli threads list

# Get thread details
uv run meter-cli threads show --thread-id "<thread-id>"

# Export thread as mbox
uv run meter-cli threads export --thread-id "<thread-id>" --format mbox
```

## Development Workflow

### 1. Create Feature Branch

```bash
# IMPORTANT: Use timestamp-based branch naming (YYYY-MM-DD-HH-MM-SS)
git checkout -b $(date +"%Y-%m-%d-%H-%M-%S")-add-export-feature

# Or use the helper script
./scripts/create-new-feature.sh "add-export-feature"
# Creates: 2025-09-11-14-30-45-add-export-feature
```

### 2. Write Tests First (TDD)

```bash
# Create failing test
cat > tests/integration/test_new_feature.py << 'EOF'
def test_new_feature():
    """Test that new feature works as expected"""
    result = process_new_feature()
    assert result.success == True
    assert result.data is not None
EOF

# Run test (should fail)
uv run pytest tests/integration/test_new_feature.py
```

### 3. Implement Feature

```bash
# Implement in appropriate module
vim src/services/new_feature.py

# Run tests again (should pass)
uv run pytest tests/integration/test_new_feature.py
```

### 4. Update Documentation

```bash
# Update CLAUDE.md with new commands
vim CLAUDE.md

# Update this quickstart if needed
vim specs/002-claude-md-project/quickstart.md
```

### 5. Commit and Push Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add export feature for meter readings

- Implement CSV, Excel, and JSON export formats
- Add CLI command: meter-cli export
- Add API endpoint: /api/export
- Include tests and documentation"

# Push to remote (branch name includes timestamp)
git push -u origin $(git branch --show-current)
```

### 6. Create Pull Request

```bash
# Create PR to main branch
gh pr create \
  --title "Add export feature for meter readings" \
  --body "Implements multiple export formats with tests and documentation" \
  --base main

# IMPORTANT: Never delete feature branches after merge
# They serve as historical point-in-time references
```

## UV Package Management

### Adding Dependencies

```bash
# NEVER use pip directly - always use UV
# Add production dependency
uv pip install fastapi
uv pip freeze > requirements.txt

# Add development dependency
uv pip install pytest --dev
uv pip freeze --dev > requirements-dev.txt
```

### Managing Virtual Environment

```bash
# Create new virtual environment
uv venv

# Activate environment
source .venv/bin/activate  # Linux/macOS

# Sync dependencies
uv pip sync requirements.txt

# Upgrade all packages
uv pip install --upgrade -r requirements.txt
```

### UV Best Practices

```bash
# Compile dependencies with version resolution
uv pip compile pyproject.toml -o requirements.txt

# Install exact versions from lock file
uv pip sync requirements.txt

# Show dependency tree
uv pip tree

# Check for security vulnerabilities
uv pip audit
```

## Performance Testing

```bash
# Generate test emails
python scripts/generate_test_emails.py --count 1000

# Run performance test
time uv run meter-cli process --batch-size 100

# Monitor resource usage
htop  # In another terminal

# Profile code
uv run python -m cProfile -o profile.stats src/cli/meter_cli.py process
uv run python -m pstats profile.stats
```

## Deployment

### Docker

```bash
# Build container
docker build -t kyocera-meter-reader .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/emails:/app/emails \
  -v $(pwd)/devices:/app/devices \
  -v $(pwd)/database:/app/database \
  --name meter-reader \
  kyocera-meter-reader

# View logs
docker logs -f meter-reader
```

### Systemd Service

```bash
# Create service file
sudo cat > /etc/systemd/system/meter-reader.service << 'EOF'
[Unit]
Description=Kyocera Meter Reader API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/kyocera-meter-reader
ExecStart=/opt/kyocera-meter-reader/.venv/bin/uvicorn src.api.meter_api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable meter-reader
sudo systemctl start meter-reader
sudo systemctl status meter-reader
```

## Support

### Logs Location
- Application logs: `logs/app.log`
- Processing logs: `logs/processing.log`
- Error logs: `logs/error.log`

### Common Issues

**Issue**: Email not processing  
**Solution**: Check quarantine folder and logs for errors

**Issue**: Duplicate readings  
**Solution**: System auto-appends _1, _2 to filenames

**Issue**: Missing device serial  
**Solution**: Check email format matches expected patterns

**Issue**: Database locked  
**Solution**: Ensure only one process accesses database

### Getting Help

1. Check logs for error details
2. Run diagnostic command: `uv run meter-cli diagnose`
3. Review documentation in `/docs`
4. Check existing issues on GitHub

---
*For detailed API documentation, visit http://localhost:8000/docs after starting the API server*