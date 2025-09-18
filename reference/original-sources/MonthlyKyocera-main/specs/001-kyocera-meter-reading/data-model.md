# Data Model: Kyocera Meter Reading Management System

**Date**: 2025-09-09
**Feature**: 001-kyocera-meter-reading

## Core Entities

### MeterReadingEmail
**Purpose**: Represents an incoming email containing device meter information

**Attributes**:
- `file_path`: str - Path to .eml file
- `received_date`: datetime - When email was received
- `subject`: str - Email subject line
- `sender`: str - Email sender address
- `body_text`: str - Plain text content
- `body_html`: str (optional) - HTML content if present
- `attachments`: list[str] - List of attachment filenames
- `processing_status`: enum - PENDING, PROCESSED, FAILED, QUARANTINED
- `processing_timestamp`: datetime - When processed
- `error_message`: str (optional) - Error details if failed

**Validation Rules**:
- file_path must exist and be readable
- file_path must have .eml extension
- received_date cannot be future date
- subject and sender cannot be empty

### Device
**Purpose**: Represents a Kyocera office device with maintenance history

**Attributes**:
- `serial_number`: str - Unique device identifier
- `model`: str - Device model (e.g., "TASKalfa-5004i")
- `first_seen`: datetime - First meter reading date
- `last_seen`: datetime - Most recent meter reading
- `status`: enum - ACTIVE, INACTIVE, RETIRED
- `location`: str (optional) - Physical location/department
- `total_readings`: int - Count of meter readings
- `folder_path`: str - Path to device folder

**Validation Rules**:
- serial_number must match pattern: [A-Z0-9]{6,20}
- model must be non-empty
- last_seen >= first_seen
- total_readings >= 0
- folder_path must follow pattern: devices/{model}/{serial_number}

### MeterReading
**Purpose**: Extracted meter reading data from an email

**Attributes**:
- `reading_id`: str - Unique identifier (UUID)
- `device_serial`: str - Device serial number
- `device_model`: str - Device model
- `reading_date`: date - Date of meter reading
- `color_count`: int (optional) - Color page count
- `mono_count`: int (optional) - Black & white page count
- `total_count`: int - Total page count
- `source_email`: str - Path to source .eml file
- `created_at`: datetime - When record created
- `pdf_path`: str - Path to generated PDF
- `txt_path`: str - Path to text file

**Validation Rules**:
- reading_date cannot be future date
- counts must be >= 0
- total_count >= color_count + mono_count (if both present)
- source_email must exist
- pdf_path and txt_path must exist after processing

**State Transitions**:
```
Created → Validated → Stored → Archived
         ↓
      Invalid → Quarantined
```

### ProcessingLog
**Purpose**: Audit trail of all system operations

**Attributes**:
- `log_id`: str - Unique identifier (UUID)
- `timestamp`: datetime - When event occurred
- `operation`: str - Operation type (PARSE, EXTRACT, CONVERT, STORE, ERROR)
- `target`: str - File or device being processed
- `status`: enum - SUCCESS, WARNING, ERROR
- `message`: str - Human-readable description
- `details`: dict - Additional context (JSON)
- `correlation_id`: str - Groups related operations

**Validation Rules**:
- timestamp must be UTC
- operation must be predefined type
- message cannot be empty
- correlation_id links related operations

### DeviceFolder
**Purpose**: Organized storage location for device readings

**Attributes**:
- `base_path`: str - Root devices folder
- `model_folder`: str - Model-specific folder
- `serial_folder`: str - Device-specific folder
- `date_folders`: list[str] - Date-based subfolders
- `file_count`: int - Total files in folder
- `last_modified`: datetime - Last update time
- `size_bytes`: int - Total folder size

**Validation Rules**:
- Folder structure: {base_path}/{model_folder}/{serial_folder}/{YYYY-MM-DD}/
- model_folder must be sanitized (no special chars except dash/underscore)
- serial_folder must match device serial
- date_folders format: YYYY-MM-DD

## Relationships

```
MeterReadingEmail (1) → (0..n) MeterReading
                 ↓
                (1) ProcessingLog (n)

Device (1) → (n) MeterReading
       (1) → (1) DeviceFolder

DeviceFolder (1) → (n) MeterReading files
```

## File Naming Conventions

### Meter Reading Files
Pattern: `{email_date}_{model}_{serial}_{process_date}_meter_reading.{ext}`

Examples:
- `2025-01-15_TASKalfa-5004i_ABC123_2025-01-16_meter_reading.pdf`
- `2025-01-15_TASKalfa-5004i_ABC123_2025-01-16_meter_reading.txt`

### Duplicate Handling
Pattern: `{base_name}_{sequence}.{ext}`

Examples:
- `..._meter_reading_1.pdf` (first duplicate)
- `..._meter_reading_2.pdf` (second duplicate)

### Processing Logs
Pattern: `processing_{YYYY-MM-DD}.json`

Example:
- `logs/processing_2025-01-16.json`

## Data Persistence

### File System Layout
```
project_root/
├── devices/                 # All device data
│   ├── TASKalfa-5004i/
│   │   ├── ABC123/
│   │   │   ├── 2025-01-15/
│   │   │   │   ├── *.pdf
│   │   │   │   └── *.txt
│   │   │   └── 2025-02-15/
│   │   └── DEF456/
│   └── TASKalfa-5054ci/
├── emails/                  # Input emails
│   ├── pending/            # To be processed
│   ├── processed/          # Successfully processed
│   └── quarantine/         # Failed processing
├── logs/                   # Processing logs
│   └── processing_*.json
└── reports/                # Generated reports
    └── SUMMARY.md
```

### Data Retention
- **Meter readings**: 24 months rolling window
- **Processing logs**: 90 days
- **Quarantined emails**: 30 days
- **Processed emails**: 7 days (then archived)

## Validation Schema

### Email Parsing
```python
{
    "required": ["subject", "sender", "received_date", "body"],
    "properties": {
        "subject": {"type": "string", "minLength": 1},
        "sender": {"type": "string", "format": "email"},
        "received_date": {"type": "string", "format": "date-time"},
        "body": {"type": "string"}
    }
}
```

### Device Identification
```python
{
    "serial_pattern": r"[A-Z0-9]{6,20}",
    "model_pattern": r"TASKalfa-[0-9]{4}[ci]{0,2}",
    "extraction_sources": ["subject", "body", "filename"]
}
```

### Meter Reading Extraction
```python
{
    "patterns": {
        "date": r"\d{4}-\d{2}-\d{2}",
        "counter": r"(Color|Mono|Total):\s*(\d+)",
        "serial": r"Serial:\s*([A-Z0-9]+)"
    }
}
```

## Error Handling States

### Email Processing Errors
- **PARSE_ERROR**: Cannot read .eml file
- **MISSING_DEVICE**: No device identifiers found
- **INVALID_DATE**: Cannot determine reading date
- **DUPLICATE_READING**: Same device/date already exists

### Recovery Actions
- **PARSE_ERROR** → Move to quarantine, log error
- **MISSING_DEVICE** → Flag for manual review
- **INVALID_DATE** → Use email received date
- **DUPLICATE_READING** → Add sequence number

## Performance Considerations

### Indexing Strategy
- Device lookups by serial (O(1) via folder structure)
- Date range queries via folder traversal
- Recent readings cached in memory

### Optimization Points
- Batch PDF generation (10 files at a time)
- Parallel email parsing (up to 4 threads)
- Lazy loading of email attachments
- Incremental summary generation

## Security & Privacy

### Data Classification
- **Public**: Device models, counts
- **Internal**: Serial numbers, locations
- **Confidential**: Email addresses, raw email content

### Access Control
- Read-only for meter data after creation
- Audit log append-only
- Quarantine folder restricted access

### Data Sanitization
- Remove email headers with PII
- Sanitize filenames (no path traversal)
- Validate all user inputs