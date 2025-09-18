# Implementation Plan: Kyocera Meter Reading Management System

**Branch**: `002-claude-md-project` | **Date**: 2025-09-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-claude-md-project/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Building a comprehensive meter reading management system that automates processing of monthly Kyocera device meter readings from emails. The system organizes readings by device (model/serial/date), generates multiple output formats (PDF/TXT/MD/YAML), provides TUI and web interfaces for management, and maintains a searchable DuckDB archive. Technical approach uses Python 3.11 with UV package manager, Textual for TUI, FastAPI for REST API, Astro + shadcn/ui for web dashboard, and follows TDD methodology with contract-first design.

## Technical Context
**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, Textual, DuckDB, fpdf2, pyyaml, rich, uvicorn  
**Storage**: DuckDB for archive, filesystem for organized meter readings  
**Testing**: pytest with pytest-asyncio, pytest-cov  
**Target Platform**: Linux server (primary), cross-platform Python support
**Project Type**: web (backend API + Astro frontend dashboard)  
**Performance Goals**: 100 emails/minute processing, <3 seconds per email  
**Constraints**: <1 second PDF generation, support 50+ devices, 24-month data retention, no file size limits for .eml processing  
**Scale/Scope**: 10 concurrent web users (initial), hundreds of monthly readings, 50+ devices, compress/archive emails to <10MB where possible

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 3 (backend api, cli, tests) ✓
- Using framework directly? Yes - FastAPI, Textual, DuckDB used directly ✓
- Single data model? Yes - shared models across services ✓
- Avoiding patterns? Yes - no unnecessary abstractions ✓

**Architecture**:
- EVERY feature as library? Yes - organized as service modules ✓
- Libraries listed:
  - email_parser: Extract data from .eml files
  - device_extractor: Pattern matching for device info
  - pdf_converter: Generate PDF reports
  - folder_manager: Directory organization
  - archive_manager: DuckDB operations
  - meter_processor: Main orchestration
- CLI per library: meter-cli with subcommands ✓
- Library docs: Will follow llms.txt format ✓

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? Yes - tests written first ✓
- Git commits show tests before implementation? Will be enforced ✓
- Order: Contract→Integration→E2E→Unit strictly followed? Yes ✓
- Real dependencies used? Yes - actual DuckDB, real files ✓
- Integration tests for: new libraries, contract changes, shared schemas? Yes ✓
- FORBIDDEN: Implementation before test, skipping RED phase - Understood ✓

**Observability**:
- Structured logging included? Yes - JSON structured logging ✓
- Frontend logs → backend? Yes - unified logging stream ✓
- Error context sufficient? Yes - comprehensive error details ✓

**Versioning**:
- Version number assigned? Yes - 1.0.0 in pyproject.toml ✓
- BUILD increments on every change? Will be tracked ✓
- Breaking changes handled? Migration plan included ✓

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: Option 2 (Web application) - Backend API + Frontend Dashboard

## Phase 0: Outline & Research
1. **Clarifications Resolved**:
   - Data retention: 24 months (configurable)
   - Concurrent users: 10 initially (scalable architecture)
   - Email security: Standard .eml file processing, no authentication required
   - Backup strategy: Multiple formats (MD, YAML) + DuckDB archive
   - Web auth: Basic authentication for dashboard (future enhancement)
   - File size handling: No limits on input .eml files, compress to <10MB for archive
   - Email reconstruction: Full email thread preservation and reconstruction capability
   - Character encoding: UTF-8 with fallback to detected encoding
   - Git workflow: YYYY-MM-DD-HH-MM-SS-description branch naming, preserve all branches

2. **Technology Research Completed**:
   - Email parsing: Python email library (standard, robust)
   - TUI framework: Textual chosen over Rich (better architecture)
   - Database: DuckDB for analytics (columnar storage, embedded)
   - Web framework: Astro + shadcn/ui (modern, performant)
   - PDF generation: fpdf2 (pure Python, no external deps)

3. **Best Practices Identified**:
   - Email processing: Parse headers first, validate structure
   - Pattern matching: Multi-source extraction with fallbacks
   - File organization: Immutable structure after processing
   - Error handling: Quarantine pattern with detailed logging

**Output**: research.md with all clarifications and decisions documented

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Entities Extracted** → `data-model.md`:
   - Device: model, serial_number, location, status, last_reading_date
   - MeterReading: device_id, reading_date, counters, source_email, file_paths
   - EmailMessage: received_date, sender, subject, body, attachments, processing_status, message_id, in_reply_to, references, thread_id
   - EmailThread: thread_id, root_message_id, subject, participant_count, message_count, last_activity
   - CompressedEmail: original_message_id, compression_method, compressed_data, original_size, compressed_size, metadata_json
   - Report: report_type, device_id, date_range, format, content
   - ProcessingLog: timestamp, action, status, error_details, file_path

2. **API Contracts Defined** → `/contracts/api-spec.yaml`:
   - POST /api/emails/process - Process pending emails (no size limit)
   - GET /api/devices - List all devices
   - GET /api/devices/{serial}/readings - Get device readings
   - GET /api/reports/generate - Generate reports
   - GET /api/dashboard/stats - Dashboard statistics
   - GET /api/logs - Processing logs
   - GET /api/emails/{message_id}/reconstruct - Reconstruct original email
   - GET /api/emails/threads/{thread_id} - Get email thread
   - POST /api/emails/compress - Compress email for storage

3. **Database Schema** → `/contracts/schema.sql`:
   - devices table with unique serial constraint
   - meter_readings table with device FK
   - email_messages table for audit trail with thread tracking
   - email_threads table for conversation management
   - compressed_emails table for archived storage
   - processing_logs table for operations
   - Indexes on date, serial, status, message_id, thread_id fields

4. **Test Scenarios Extracted**:
   - Email processing flow test
   - Duplicate handling test
   - Quarantine scenario test
   - Report generation test
   - Dashboard data aggregation test

5. **CLAUDE.md Updated**:
   - Already contains project context
   - Technology stack documented
   - Commands and workflow defined
   - Keep under 150 lines

**Output**: data-model.md, /contracts/*, quickstart.md created

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none required)

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*