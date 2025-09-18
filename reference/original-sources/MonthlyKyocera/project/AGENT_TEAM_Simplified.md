Based on the MonthlyKyocera AGENT_TEAM_STRUCTURE.md document, here's the hierarchical team structure with numbered agents for your Claude Code implementation:

## **Kyocera Meter Reading Management System - Agent Hierarchy**

### **000 - Project Coordination (Orchestrator)**
- **000-project-orchestrator** (Sonnet) - Development Phase Coordinator

### **001-003 - Strategic Advisory (Think-Tank)**
- **001-strategy-advisor** (Sonnet) - Strategic Planning Specialist
- **002-pattern-analyst** (Sonnet) - Pattern Recognition Specialist  
- **003-quality-auditor** (Sonnet) - Quality Assurance Strategist

### **004-008 - Senior Tech Leads (Architecture)**
- **004-devops-architect** (Sonnet) - DevOps & Infrastructure Lead *(Phase 3.1: Setup)*
- **005-test-architect** (Sonnet) - Test Strategy Lead *(Phase 3.2: Tests First)*
- **006-backend-architect** (Sonnet) - Backend Architecture Lead *(Phase 3.3: Core Implementation)*
- **007-email-processing-lead** (Sonnet) - Email Processing Domain Expert *(Phase 3.3: Core Implementation)*
- **008-api-architect** (Sonnet) - API Design Lead *(Phase 3.3: Core Implementation)*

### **009-011 - Infrastructure Team (Setup Phase)**
- **009-setup-engineer** (Haiku) - Environment Setup Developer
- **010-dependency-manager** (Haiku) - Dependency Management Specialist
- **011-database-engineer** (Haiku) - Database Specialist

### **012-016 - Testing Team (Tests First Phase)**
- **012-contract-tester** (Haiku) - Contract Test Developer
- **013-integration-tester** (Haiku) - Integration Test Developer
- **014-unit-tester** (Haiku) - Unit Test Developer
- **015-performance-tester** (Haiku) - Performance Test Developer

### **016-019 - Core Backend Development Team (Implementation Phase)**
- **016-model-builder** (Haiku) - Data Model Developer
- **017-service-developer** (Haiku) - Business Logic Developer
- **018-cli-developer** (Haiku) - CLI Command Developer

### **019-021 - Email Processing Team (Implementation Phase)**
- **019-email-parser-dev** (Haiku) - Email Parser Developer
- **020-compression-specialist** (Haiku) - Compression Developer
- **021-thread-manager-dev** (Haiku) - Thread Management Developer

### **022-024 - API Development Team (Implementation Phase)**
- **022-api-developer** (Haiku) - REST API Developer
- **023-endpoint-specialist** (Haiku) - Endpoint Optimization Developer
- **024-middleware-developer** (Haiku) - Middleware Developer

### **025-027 - Infrastructure Support Team (Integration Phase)**
- **025-git-specialist** (Haiku) - Git Workflow Developer
- **026-logger-specialist** (Haiku) - Logging Infrastructure Developer

### **027-028 - Documentation & Quality Team (Polish Phase)**
- **027-doc-writer** (Haiku) - Documentation Specialist
- **028-cleanup-specialist** (Haiku) - Code Quality Developer

## **Development Phase Usage Guide**

### **Phase 3.1: Setup (000, 004, 009-011)**
```bash
# Start with orchestrator to plan setup
000-project-orchestrator → 004-devops-architect → 009-011 (parallel execution)
```

### **Phase 3.2: Tests First (000, 005, 012-015)**
```bash
# Orchestrator coordinates TDD implementation
000-project-orchestrator → 005-test-architect → 012-015 (parallel execution)
```

### **Phase 3.3: Core Implementation (000, 006-008, 016-024)**
```bash
# Major implementation phase with multiple teams
000-project-orchestrator → 006-008 (Senior Leads) → 016-024 (Junior teams)
```

### **Phase 3.4: Integration (000, 004, 006-007, 025-026)**
```bash
# Integration and infrastructure finalization
000-project-orchestrator → 004,006,007 (coordination) → 025-026 (support)
```

### **Phase 3.5: Polish (000, 005, 008, 027-028)**
```bash
# Final testing, documentation, and cleanup
000-project-orchestrator → 005,008 (leads) → 027-028 (finalization)
```

## **Usage Example for Claude Code**

```bash
# Phase 3.1 - Setup
claude-agent 000-project-orchestrator --task "Initialize Phase 3.1"
claude-agent 004-devops-architect --task "Plan infrastructure setup"
claude-agent 009-setup-engineer --task "T001: Create project structure"
claude-agent 010-dependency-manager --task "T002-T004: UV environment setup"
claude-agent 011-database-engineer --task "T007: DuckDB schema"

# Phase 3.2 - Tests First  
claude-agent 000-project-orchestrator --task "Initialize Phase 3.2"
claude-agent 005-test-architect --task "Design TDD strategy"
claude-agent 012-contract-tester --task "T008-T017: API contract tests"
```

This numbering system follows the development workflow from orchestration (000) → strategy (001-003) → phase leadership (004-008) → implementation teams (009-028), allowing you to clearly see the execution order and dependencies in your Claude Code implementation.
