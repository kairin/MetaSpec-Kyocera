# Quick Start Guide: Kyocera Meter Reading Management System

## Installation

### Prerequisites
- Python 3.11 or higher
- 1GB free disk space
- Read/write permissions to installation directory

### Install Steps
```bash
# Clone repository
git clone <repository-url>
cd kyocera-meter-reader

# Install dependencies
pip install -r requirements.txt

# Verify installation
meter-cli --version
# Expected: meter-cli version 1.0.0
```

## Basic Usage

### 1. Setup Folder Structure
```bash
# Create required directories
meter-cli validate --repair

# This creates:
# ./devices/      - Processed meter readings
# ./emails/       - Input email directory
#   ├── pending/  - Emails to process
#   ├── processed/- Successfully processed
#   └── quarantine/ - Failed processing
# ./logs/         - Processing logs
# ./reports/      - Generated reports
```

### 2. Process Your First Email
```bash
# Place .eml files in emails/pending/
cp ~/Downloads/*.eml ./emails/pending/

# Process all pending emails
meter-cli process

# Output:
# Processing 3 emails...
# ✓ TASKalfa-5004i_ABC123_2025-01-15.eml → devices/TASKalfa-5004i/ABC123/2025-01-15/
# ✓ TASKalfa-5054ci_DEF456_2025-01-15.eml → devices/TASKalfa-5054ci/DEF456/2025-01-15/
# ✓ TASKalfa-5004i_GHI789_2025-01-15.eml → devices/TASKalfa-5004i/GHI789/2025-01-15/
# 
# Summary: 3 processed, 0 failed
```

### 3. View Processed Readings
```bash
# List all devices
meter-cli list --type=devices

# Output:
# Model           Serial    Last Reading    Total Readings
# -------------  --------  --------------  ----------------
# TASKalfa-5004i  ABC123    2025-01-15      12
# TASKalfa-5004i  GHI789    2025-01-15      8
# TASKalfa-5054ci  DEF456    2025-01-15      15

# View specific device readings
ls -la devices/TASKalfa-5004i/ABC123/
```

### 4. Generate Reports
```bash
# Generate monthly summary
meter-cli report --start-date=2025-01-01 --end-date=2025-01-31

# View report
cat reports/SUMMARY.md
```

## Common Scenarios

### Scenario 1: Batch Processing Monthly Emails
```bash
# Download all meter reading emails from Outlook
# Save them to a temporary folder
mkdir ~/meter-emails-jan-2025
# ... save emails from Outlook ...

# Process the batch
meter-cli process --input=~/meter-emails-jan-2025 --verbose

# Check for any failures
ls -la emails/quarantine/
```

### Scenario 2: Handle Processing Errors
```bash
# If emails fail processing, check quarantine
meter-cli parse emails/quarantine/failed-email.eml

# Common issues:
# - Missing device serial: Manual review needed
# - Corrupted file: Re-export from email client
# - Duplicate reading: Check if already processed

# After fixing, move back to pending
mv emails/quarantine/fixed-email.eml emails/pending/
meter-cli process
```

### Scenario 3: Validate Data Integrity
```bash
# Regular validation (weekly recommended)
meter-cli validate

# If issues found, attempt repair
meter-cli validate --repair

# Check processing logs for details
tail -f logs/processing_$(date +%Y-%m-%d).json
```

### Scenario 4: Find Specific Readings
```bash
# Find readings for specific device
find devices/ -name "*ABC123*" -type d

# Search by date
find devices/ -name "2025-01-*" -type d

# Get device history
meter-cli report --device=ABC123
```

## Troubleshooting

### Email Not Processing
```bash
# Debug parse single email
meter-cli parse emails/pending/problem.eml --format=json

# Check for:
# - Valid .eml format
# - Device identifiers in subject/body
# - Readable file permissions
```

### Duplicate Readings
```bash
# System auto-handles duplicates by appending _1, _2, etc.
# To check for duplicates:
find devices/ -name "*_[0-9].pdf" 

# Review and remove if needed
```

### Storage Issues
```bash
# Check disk usage
du -sh devices/

# Archive old readings (>24 months)
find devices/ -type d -name "2023-*" -exec tar -czf archive-2023.tar.gz {} +
find devices/ -type d -name "2023-*" -exec rm -rf {} \;
```

### Performance Issues
```bash
# Process in smaller batches
ls emails/pending/*.eml | head -50 | xargs -I {} mv {} emails/batch/
meter-cli process --input=emails/batch/

# Enable parallel processing (future feature)
# meter-cli process --parallel --max-workers=4
```

## Testing the Installation

### Run Validation Tests
```bash
# 1. Test email parsing
echo "Test email content" > test.txt
meter-cli parse test.eml 2>&1 | grep "error"
# Expected: Error about invalid format

# 2. Test folder creation
meter-cli validate --repair --dry-run
# Expected: Shows what would be created

# 3. Test with sample email
# Download sample from: docs/samples/sample-meter-reading.eml
meter-cli process --input=docs/samples/ --dry-run
# Expected: Shows processing without changes

# 4. Verify PDF generation
meter-cli process --input=docs/samples/
ls devices/*/*/2025-*/
# Expected: Both .pdf and .txt files created
```

## Configuration

### Default Settings
```yaml
# config.yaml (optional)
processing:
  input_dir: ./emails/pending
  output_dir: ./devices
  parallel: false
  skip_duplicates: true

retention:
  meter_readings_months: 24
  logs_days: 90
  quarantine_days: 30

logging:
  level: INFO
  format: json
  rotate_daily: true
```

### Environment Variables
```bash
export METER_CLI_CONFIG=/path/to/config.yaml
export METER_CLI_LOG_LEVEL=DEBUG
export METER_CLI_OUTPUT_DIR=/custom/path
```

## Next Steps

1. **Schedule Automation**: Set up cron job for daily processing
   ```bash
   # Add to crontab
   0 9 * * * /usr/bin/meter-cli process >> /var/log/meter-cli.log 2>&1
   ```

2. **Monitor Health**: Check logs regularly
   ```bash
   meter-cli validate
   tail -f logs/processing_*.json
   ```

3. **Generate Reports**: Monthly reporting
   ```bash
   # First of each month
   meter-cli report --start-date=$(date -d "1 month ago" +%Y-%m-01)
   ```

## Support

- Check logs: `logs/processing_YYYY-MM-DD.json`
- Validate structure: `meter-cli validate`
- Debug mode: `meter-cli --log-level=DEBUG process`
- Sample files: `docs/samples/`

## Quick Reference

| Command | Purpose |
|---------|---------|
| `meter-cli process` | Process pending emails |
| `meter-cli validate` | Check folder structure |
| `meter-cli report` | Generate summary |
| `meter-cli list` | Show devices/readings |
| `meter-cli parse <file>` | Debug single email |
| `meter-cli --help` | Show all commands |