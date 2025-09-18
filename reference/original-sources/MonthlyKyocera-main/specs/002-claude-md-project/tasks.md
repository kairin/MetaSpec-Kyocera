# Tasks: Kyocera Meter Reading Management System

**Input**: Design documents from `/specs/002-claude-md-project/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Tech stack: Python 3.11, UV, FastAPI, Textual, DuckDB, fpdf2
   → Structure: Web application (backend/frontend split)
2. Load optional design documents:
   → data-model.md: 7 entities extracted (Device, MeterReading, EmailMessage, EmailThread, CompressedEmail, Report, ProcessingLog)
   → contracts/: api-spec.yaml (14 endpoints), schema.sql (7 tables)
   → research.md: Technology decisions documented
3. Generate tasks by category:
   → Setup: UV environment, project structure, dependencies
   → Tests: 14 contract tests, 5 integration tests
   → Core: 7 models, 6 services, CLI commands
   → Integration: DuckDB setup, middleware, logging
   → Polish: unit tests, performance, documentation
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001-T050)
6. Return: SUCCESS (50 tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/` (future Astro implementation)
- **Scripts**: `scripts/` (existing Phase 1 scripts)

## Phase 3.1: Setup
- [ ] T001 Create backend project structure (backend/src/{models,services,api,cli,lib})
- [ ] T002 Initialize UV virtual environment with `uv venv` in project root
- [ ] T003 Install core dependencies via UV: `uv pip install fastapi uvicorn duckdb fpdf2 pyyaml textual rich python-dateutil`
- [ ] T004 [P] Install dev dependencies via UV: `uv pip install pytest pytest-asyncio pytest-cov black ruff mypy httpx`
- [ ] T005 [P] Configure pytest.ini and test structure in backend/tests/{contract,integration,unit}
- [ ] T006 [P] Setup ruff.toml and black configuration for code formatting
- [ ] T007 [P] Initialize DuckDB database at database/meter_readings.duckdb with schema.sql

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests (API Endpoints)
- [ ] T008 [P] Contract test POST /emails/process in backend/tests/contract/test_emails_process.py
- [ ] T009 [P] Contract test GET /emails/{message_id}/reconstruct in backend/tests/contract/test_emails_reconstruct.py
- [ ] T010 [P] Contract test GET /emails/threads/{thread_id} in backend/tests/contract/test_emails_threads.py
- [ ] T011 [P] Contract test POST /emails/compress in backend/tests/contract/test_emails_compress.py
- [ ] T012 [P] Contract test GET /devices in backend/tests/contract/test_devices_list.py
- [ ] T013 [P] Contract test GET /devices/{serial} in backend/tests/contract/test_devices_get.py
- [ ] T014 [P] Contract test GET /devices/{serial}/readings in backend/tests/contract/test_devices_readings.py
- [ ] T015 [P] Contract test POST /reports/generate in backend/tests/contract/test_reports_generate.py
- [ ] T016 [P] Contract test GET /dashboard/stats in backend/tests/contract/test_dashboard_stats.py
- [ ] T017 [P] Contract test GET /logs in backend/tests/contract/test_logs.py

### Integration Tests (User Stories)
- [ ] T018 [P] Integration test: Process email with meter reading in backend/tests/integration/test_email_processing_flow.py
- [ ] T019 [P] Integration test: Handle duplicate readings in backend/tests/integration/test_duplicate_handling.py
- [ ] T020 [P] Integration test: Quarantine invalid emails in backend/tests/integration/test_quarantine_flow.py
- [ ] T021 [P] Integration test: Email thread reconstruction in backend/tests/integration/test_thread_reconstruction.py
- [ ] T022 [P] Integration test: Email compression and archival in backend/tests/integration/test_compression_flow.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Models
- [ ] T023 [P] Device model in backend/src/models/device.py
- [ ] T024 [P] MeterReading model in backend/src/models/meter_reading.py
- [ ] T025 [P] EmailMessage model with threading fields in backend/src/models/email_message.py
- [ ] T026 [P] EmailThread model in backend/src/models/email_thread.py
- [ ] T027 [P] CompressedEmail model in backend/src/models/compressed_email.py
- [ ] T028 [P] Report model in backend/src/models/report.py
- [ ] T029 [P] ProcessingLog model in backend/src/models/processing_log.py

### Service Layer
- [ ] T030 EmailParser service for .eml parsing in backend/src/services/email_parser.py
- [ ] T031 DeviceExtractor service for serial extraction in backend/src/services/device_extractor.py
- [ ] T032 PDFConverter service for PDF generation in backend/src/services/pdf_converter.py
- [ ] T033 FolderManager service for directory ops in backend/src/services/folder_manager.py
- [ ] T034 ArchiveManager service for DuckDB operations in backend/src/services/archive_manager.py
- [ ] T035 CompressionService for email compression in backend/src/services/compression_service.py
- [ ] T036 ThreadManager service for email threads in backend/src/services/thread_manager.py

### API Endpoints
- [ ] T037 POST /emails/process endpoint in backend/src/api/emails.py
- [ ] T038 GET /emails/{message_id}/reconstruct endpoint in backend/src/api/emails.py
- [ ] T039 GET /emails/threads/{thread_id} endpoint in backend/src/api/emails.py
- [ ] T040 POST /emails/compress endpoint in backend/src/api/emails.py
- [ ] T041 GET /devices endpoints in backend/src/api/devices.py
- [ ] T042 GET /devices/{serial}/readings endpoint in backend/src/api/devices.py
- [ ] T043 POST /reports/generate endpoint in backend/src/api/reports.py
- [ ] T044 GET /dashboard/stats endpoint in backend/src/api/dashboard.py
- [ ] T045 GET /logs endpoint in backend/src/api/logs.py

### CLI Commands
- [ ] T046 meter-cli process command in backend/src/cli/meter_cli.py
- [ ] T047 meter-cli validate command in backend/src/cli/meter_cli.py
- [ ] T048 meter-cli report command in backend/src/cli/meter_cli.py

## Phase 3.4: Integration
- [ ] T049 Connect all services to DuckDB with connection pooling
- [ ] T050 Setup structured JSON logging with error context
- [ ] T051 Implement email quarantine workflow with detailed error logging
- [ ] T052 Configure FastAPI middleware for CORS and request logging
- [ ] T053 Implement git branch creation with YYYY-MM-DD-HH-MM-SS format

## Phase 3.5: Polish
- [ ] T054 [P] Unit tests for DeviceExtractor patterns in backend/tests/unit/test_device_extractor.py
- [ ] T055 [P] Unit tests for email parsing edge cases in backend/tests/unit/test_email_parser.py
- [ ] T056 [P] Unit tests for compression algorithms in backend/tests/unit/test_compression.py
- [ ] T057 Performance tests: 100 emails/minute processing
- [ ] T058 Performance tests: <3 second per email processing
- [ ] T059 [P] Update CLAUDE.md with implementation details
- [ ] T060 [P] Create API documentation in docs/api.md
- [ ] T061 Run quickstart.md validation tests
- [ ] T062 Cleanup and refactor duplicated code

## Dependencies
- Setup (T001-T007) must complete first
- Contract/Integration tests (T008-T022) before ANY implementation
- Models (T023-T029) can be parallel but before services
- Services (T030-T036) before API endpoints
- API endpoints (T037-T045) require services
- CLI (T046-T048) can parallel with API
- Integration (T049-T053) after core implementation
- Polish (T054-T062) last

## Parallel Execution Examples

### Initial Setup (can run together):
```bash
# Launch T003-T007 together after T001-T002:
uv run python -m Task "Install dev dependencies via UV"
uv run python -m Task "Configure pytest.ini and test structure"
uv run python -m Task "Setup ruff.toml and black configuration"
uv run python -m Task "Initialize DuckDB database with schema"
```

### Contract Tests (all can run in parallel):
```bash
# Launch T008-T017 together:
uv run python -m Task "Contract test POST /emails/process"
uv run python -m Task "Contract test GET /emails reconstruct"
uv run python -m Task "Contract test GET /emails threads"
# ... etc for all contract tests
```

### Models Creation (all can run in parallel):
```bash
# Launch T023-T029 together:
uv run python -m Task "Create Device model"
uv run python -m Task "Create MeterReading model"
uv run python -m Task "Create EmailMessage model"
# ... etc for all models
```

## Git Workflow Requirements
- Every commit creates branch: `YYYY-MM-DD-HH-MM-SS-{description}`
- Use system clock for timestamp (seconds precision required!)
- Description from commit message (kebab-case)
- NEVER delete branches (preserve history)
- Complete PRs with merge to main
- Example: `2025-09-11-14-32-45-add-email-parser-service`

## UV Package Manager Requirements
- **CRITICAL**: Use UV exclusively - NO direct pip commands
- Virtual environment: `uv venv`
- Install packages: `uv pip install {package}`
- Update requirements: `uv pip freeze > requirements.txt`
- Run commands: `uv run python {script}`
- **FORBIDDEN**: `pip install`, `python -m pip`, `pip3`

## Notes
- [P] tasks = different files, no shared dependencies
- Verify all tests fail before implementing (RED phase of TDD)
- Commit after each task with timestamped branch
- Email files have no size limit (compress for storage)
- Preserve email threads and enable reconstruction
- All operations through UV package manager

## Validation Checklist
- [x] All 14 API endpoints have contract tests
- [x] All 7 entities have model tasks
- [x] All tests come before implementation (T008-T022 before T023-T048)
- [x] Parallel tasks are truly independent (different files)
- [x] Each task specifies exact file path
- [x] No [P] task modifies same file as another [P] task
- [x] UV used exclusively for Python operations
- [x] Git branch strategy documented