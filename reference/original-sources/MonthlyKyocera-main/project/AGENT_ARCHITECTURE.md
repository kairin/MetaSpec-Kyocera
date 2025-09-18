# Agent Architecture for Kyocera Document Processing

## Overview
A multi-agent system designed to efficiently process Kyocera meter reading documents from multiple sources (scans, emails, inventory).

## Agent Hierarchy

```
┌─────────────────────────────────────┐
│       ORCHESTRATOR AGENT            │
│   (Coordinates all processing)      │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┬───────────┬────────────┐
       ▼               ▼           ▼            ▼
┌──────────┐   ┌──────────┐  ┌──────────┐  ┌──────────┐
│  SCAN    │   │  EMAIL   │  │  DATA    │  │  REPORT  │
│  AGENT   │   │  AGENT   │  │  AGENT   │  │  AGENT   │
└──────────┘   └──────────┘  └──────────┘  └──────────┘
     │              │             │              │
     ▼              ▼             ▼              ▼
[OCR/Extract] [Parse/Extract] [Validate]   [Generate]
```

## Agent Specifications

### 1. Orchestrator Agent
**Purpose**: Main coordinator that manages the entire processing pipeline

**Responsibilities**:
- Load device registry
- Distribute work to specialized agents
- Track processing status
- Handle errors and retries
- Generate final summary

**Input**: Device serial number or batch processing request
**Output**: Processing status and summary report

### 2. Scan Agent
**Purpose**: Process device screenshots from Kyocera-scan folder

**Responsibilities**:
- Read device scan images
- Extract text using OCR if needed
- Parse device status information
- Extract counter readings
- Identify toner levels

**Technologies**:
- Python PIL/Pillow for image processing
- pytesseract for OCR (if needed)
- Pattern matching for data extraction

**Input**: Path to scan images
**Output**: Structured data (JSON) with device metrics

### 3. Email Agent
**Purpose**: Process .eml and .msg email files

**Responsibilities**:
- Parse email headers and body
- Extract meter readings from email content
- Handle both counter and toner emails
- Process attachments if present
- Handle duplicates intelligently

**Technologies**:
- Python email library for .eml
- extract-msg for .msg files
- Regular expressions for data extraction

**Input**: Email file paths
**Output**: Structured meter reading data

### 4. Data Agent
**Purpose**: Validate, merge, and store processed data

**Responsibilities**:
- Validate extracted data
- Merge data from multiple sources
- Detect and handle conflicts
- Store in DuckDB database
- Maintain data integrity

**Technologies**:
- DuckDB for storage
- Data validation rules
- Conflict resolution logic

**Input**: Data from Scan and Email agents
**Output**: Validated and stored records

### 5. Report Agent
**Purpose**: Generate reports and output files

**Responsibilities**:
- Generate PDF reports
- Create text summaries
- Export to various formats (MD, YAML, CSV)
- Create visualizations
- Send notifications if configured

**Technologies**:
- fpdf2 for PDF generation
- Matplotlib for charts
- Jinja2 for templates

**Input**: Processed data from Data Agent
**Output**: Reports in multiple formats

## Processing Workflow

```python
# Example workflow for single device
workflow = {
    "device_serial": "W7F3601552",
    "steps": [
        {
            "step": 1,
            "agent": "Orchestrator",
            "action": "Load device info from registry"
        },
        {
            "step": 2,
            "agents": ["Scan", "Email"],  # Parallel processing
            "action": "Extract data from sources"
        },
        {
            "step": 3,
            "agent": "Data",
            "action": "Validate and merge data"
        },
        {
            "step": 4,
            "agent": "Report",
            "action": "Generate outputs"
        }
    ]
}
```

## Agent Communication Protocol

### Message Format
```json
{
    "agent_id": "scan_agent_001",
    "timestamp": "2025-09-11T21:00:00Z",
    "device_serial": "W7F3601552",
    "status": "processing|completed|error",
    "data": {
        "readings": {...},
        "metadata": {...}
    },
    "error": null
}
```

### Error Handling
- Automatic retry with exponential backoff
- Quarantine problematic files
- Detailed error logging
- Fallback to manual processing queue

## Implementation Files

### Core Agent Scripts
```
scripts/agents/
├── orchestrator.py       # Main coordinator
├── scan_agent.py         # Process scans
├── email_agent.py        # Process emails
├── data_agent.py         # Data validation/storage
├── report_agent.py       # Report generation
└── agent_base.py         # Base agent class
```

### Configuration
```yaml
# config/agents.yaml
agents:
  scan:
    enabled: true
    ocr_enabled: false  # Screenshots are already text
    batch_size: 10
    
  email:
    enabled: true
    formats: [eml, msg]
    batch_size: 50
    
  data:
    enabled: true
    database: duckdb
    validation_rules: strict
    
  report:
    enabled: true
    formats: [pdf, txt, md, yaml]
    template_dir: templates/
```

## Deployment Strategy

### Phase 1: Single Device Processing
- Test with one device (e.g., W7F3601552)
- Validate each agent independently
- Ensure data accuracy

### Phase 2: Batch Processing
- Process all 28 devices
- Parallel agent execution
- Performance optimization

### Phase 3: Automation
- Schedule regular processing
- Email notifications
- Dashboard integration

## Performance Targets
- Single device: < 5 seconds
- Full batch (28 devices): < 2 minutes
- Parallel processing: 4 agents concurrent
- Error rate: < 1%

## Next Steps
1. Create base agent class
2. Implement Scan Agent
3. Implement Email Agent
4. Implement Data Agent
5. Implement Report Agent
6. Create Orchestrator
7. Test with sample data
8. Full deployment