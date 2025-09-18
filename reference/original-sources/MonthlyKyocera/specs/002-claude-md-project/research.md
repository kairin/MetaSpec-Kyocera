# Research & Technology Decisions

**Feature**: Kyocera Meter Reading Management System  
**Date**: 2025-09-11  
**Status**: Complete

## Executive Summary

This document captures technology research and decisions for the Kyocera Meter Reading Management System. All clarifications from the specification have been resolved, and technology choices have been validated against project requirements and constraints.

## Clarifications Resolved

### Business Requirements

| Requirement | Clarification | Decision |
|------------|--------------|-----------|
| Data Retention Period | Not specified in original spec | **24 months** (configurable in settings) |
| Concurrent Web Users | Not specified | **10 users initially**, scalable architecture |
| Email Authentication | Security requirements unclear | Standard .eml processing, no auth required |
| Backup Strategy | Not detailed | Multiple formats (MD, YAML) + DuckDB archive |
| Web Dashboard Auth | Not specified | Basic auth initially, OAuth2 future enhancement |
| File Size Limits | Not specified | **No limits on input .eml files**, compress archives to <10MB |
| Character Encoding | International device support | UTF-8 primary, auto-detection fallback |
| Performance Monitoring | Not specified | JSON structured logging + metrics |
| API Rate Limiting | Not specified | 100 requests/minute per IP |
| Disaster Recovery | Not specified | Daily DuckDB backups, file versioning |
| Email Reconstruction | Not specified | Full email reconstruction from compressed storage |
| Thread Preservation | Not specified | Complete email thread tracking and relationships |
| Git Workflow | Not specified | YYYY-MM-DD-HH-MM-SS-description branches, never delete |

## Technology Stack Analysis

### Email Processing

**Decision**: Python `email` standard library  
**Rationale**: 
- Built-in, mature, well-documented
- Handles all .eml format variations
- No external dependencies
- Supports MIME multipart messages

**Alternatives Considered**:
- `python-magic`: Added for file type detection
- `chardet`: Added for encoding detection
- `mailparser`: Rejected - unnecessary abstraction

### TUI Framework

**Decision**: Textual  
**Rationale**:
- Modern reactive architecture
- Built-in widgets and layouts
- CSS-like styling
- Better testing support
- Active development

**Alternatives Considered**:
- Rich: Good for simple TUIs, less suitable for complex interfaces
- Curses: Too low-level, poor cross-platform support
- Urwid: Older, less modern API

### Database

**Decision**: DuckDB  
**Rationale**:
- Embedded, no server required
- Columnar storage ideal for analytics
- SQL interface familiar to users
- Excellent Python integration
- Fast aggregations for reporting

**Alternatives Considered**:
- SQLite: Row-based, slower for analytics
- PostgreSQL: Requires server, overengineered for this use case
- Parquet files: No query capability without additional tools

### PDF Generation

**Decision**: fpdf2  
**Rationale**:
- Pure Python, no system dependencies
- Simple API for basic reports
- Supports images and formatting
- Lightweight and fast

**Alternatives Considered**:
- ReportLab: More complex, overkill for simple reports
- WeasyPrint: Requires system libraries
- wkhtmltopdf: External binary dependency

### Web Framework (Backend)

**Decision**: FastAPI  
**Rationale**:
- Modern async Python framework
- Automatic OpenAPI documentation
- Type hints and validation with Pydantic
- High performance with Uvicorn
- WebSocket support for real-time updates

**Alternatives Considered**:
- Flask: Older, requires more boilerplate
- Django: Too heavyweight for API-only backend
- Starlette: Lower-level, FastAPI builds on it

### Web Dashboard (Frontend)

**Decision**: Astro + shadcn/ui  
**Rationale**:
- Astro: Static site generation, excellent performance
- shadcn/ui: Modern components, Tailwind-based
- DuckDB WASM: Query database directly from browser
- Minimal JavaScript for better performance

**Alternatives Considered**:
- Next.js: Heavier runtime, not needed for dashboard
- Vue/Nuxt: Additional framework complexity
- Plain HTML: Insufficient for interactive charts

## Best Practices & Patterns

### Email Processing Pipeline

```python
# Recommended processing flow
1. Validate .eml file structure
2. Parse headers (date, subject, sender)
3. Extract body (prefer plain text)
4. Identify device from multiple sources:
   - Email subject pattern
   - Body content patterns
   - Filename patterns
   - Sender address mapping
5. Generate unique filename
6. Create output files (PDF, TXT, MD, YAML)
7. Move to appropriate folder
8. Update database
9. Log processing result
```

### Error Handling Strategy

**Quarantine Pattern**:
- Failed emails → `/emails/quarantine/`
- Detailed error log with stack trace
- Original file preserved
- Manual review queue
- Retry mechanism after fixes

### File Organization

**Immutable After Processing**:
- Never modify processed files
- Append sequence for duplicates
- Maintain audit trail
- Use symlinks for alternate views

### Performance Optimization

**Batch Processing**:
- Process in chunks of 50 emails
- Parallel PDF generation (4 workers)
- Bulk database inserts
- Async I/O for file operations

**Caching Strategy**:
- Cache device lookup table
- Memoize regex patterns
- Connection pooling for database
- Static file caching for dashboard

## Security Considerations

### Input Validation
- Sanitize filenames (prevent path traversal)
- Validate email structure before parsing
- No size limits on input .eml files
- Compress large emails for storage
- Check file types with python-magic

### Data Protection
- No PII in logs (hash email addresses)
- Encrypted database connections
- Read-only permissions after processing
- Secure file permissions (0644)

### Web Security
- CORS configuration for API
- Rate limiting (100 req/min)
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)

## Scalability Plan

### Phase 1 (Current)
- 10 concurrent users
- 100 emails/minute
- 50 devices
- Single server deployment

### Phase 2 (6 months)
- 50 concurrent users
- 500 emails/minute
- 200 devices
- Add Redis for caching

### Phase 3 (12 months)
- 100+ concurrent users
- 1000 emails/minute
- 500+ devices
- Horizontal scaling with load balancer
- Separate database server

## Integration Points

### External Systems
- Email servers (IMAP/POP3 future)
- LDAP/AD for authentication (future)
- Billing systems via API
- Monitoring (Prometheus/Grafana)

### Data Formats
- Input: .eml (RFC 822)
- Output: PDF, TXT, Markdown, YAML
- API: JSON (REST), GraphQL (future)
- Database: DuckDB native format

## Email Compression Strategy

### Compression Methods
- **Primary**: zstd (Zstandard) - Best compression ratio and speed
- **Fallback**: gzip - Universal compatibility
- **Archive Format**: Custom format with metadata header
- **Target**: Compress emails >10MB to <10MB where possible

### Email Thread Management
- Track Message-ID, In-Reply-To, References headers
- Build thread hierarchy from relationships
- Preserve complete conversation context
- Support thread reconstruction from any message

### Reconstruction Capability
- Store all headers in metadata JSON
- Compress body and attachments separately
- Maintain MIME structure information
- Support full .eml file regeneration

## UV Package Manager Best Practices

### Exclusive UV Usage
- **NEVER** use pip directly
- All installations via `uv pip install`
- Virtual environment: `uv venv`
- Requirements: `uv pip compile`
- Lock files: `uv pip freeze`

### UV Commands
```bash
# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Install package
uv pip install package-name

# Compile requirements
uv pip compile pyproject.toml -o requirements.txt

# Sync environment
uv pip sync requirements.txt
```

### UV Configuration
```toml
# pyproject.toml
[tool.uv]
python = "3.11"
preview = true
managed = true
```

## Development Tools

### Testing
- pytest: Test framework
- pytest-asyncio: Async test support
- pytest-cov: Coverage reporting
- Hypothesis: Property-based testing (future)

### Code Quality
- Black: Code formatting
- Ruff: Fast linting
- mypy: Type checking
- pre-commit: Git hooks

## Deployment Strategy

### Containerization
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
# Install UV and dependencies
FROM python:3.11-slim
# Copy only necessary files
```

### Environment Management
- UV EXCLUSIVELY for package management (no pip)
- .env files for configuration
- Docker Compose for local development
- Kubernetes for production (future)

### Git Branch Strategy
- Format: `YYYY-MM-DD-HH-MM-SS-description`
- Timestamp from system clock at commit
- Description from commit message (kebab-case)
- NEVER delete historical branches
- Main branch remains default
- Each branch preserves point-in-time state

## Monitoring & Observability

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Correlation IDs for request tracking
- Centralized logging (ELK stack future)

### Metrics
- Processing rate (emails/minute)
- Error rate by type
- Database query performance
- API response times

### Alerting
- Failed processing threshold
- Disk space warnings
- Database connection issues
- API availability

## Migration Strategy

### From Existing System
1. Export historical data
2. Transform to new format
3. Bulk import to DuckDB
4. Validate data integrity
5. Parallel run period
6. Cutover plan

### Version Upgrades
- Database migrations with versioning
- Backward compatibility for 2 versions
- Feature flags for gradual rollout
- Automated rollback capability

## Conclusion

All technology decisions have been made with consideration for:
- Simplicity and maintainability
- Performance requirements
- Scalability needs
- Security best practices
- Developer experience

The chosen stack provides a solid foundation for the Kyocera Meter Reading Management System while maintaining flexibility for future enhancements.

---
*Next Step: Create data-model.md with entity definitions*