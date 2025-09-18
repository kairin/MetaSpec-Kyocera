# Agent Team Structure - Kyocera Meter Reading Management System

## Overview

This document defines the hierarchical team structure of AI agents responsible for implementing the Kyocera Meter Reading Management System. The structure includes an Orchestrator who coordinates development phases, a Think-Tank Advisory Group for strategic guidance, Senior Tech Leads (Claude Sonnet models) who architect solutions, and specialized Junior Developers (Claude Haiku models) for implementation.

## Team Hierarchy

```
┌─────────────────────────────────────────┐
│      CTO - Chief Technical Officer      │
│              (Human Leader)              │
└─────────────────────┬───────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐          ┌──────▼──────────┐
│  Think-Tank    │◄─────────┤  Orchestrator   │
│Advisory Group  │  consults│ (Sonnet Model)  │
│(Sonnet Models) │          │ Phase Coordinator│
└────────────────┘          └──────┬──────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
    ┌─────────▼─────────┐                    ┌─────────▼─────────┐
    │  Senior Tech Leads│                    │ Senior Tech Leads │
    │  (Sonnet Models)  │                    │ (Sonnet Models)   │
    │  Domain Experts   │                    │ Quality Experts   │
    └─────────┬─────────┘                    └─────────┬─────────┘
              │                                         │
    ┌─────────▼─────────────────────────────────────────▼─────────┐
    │                  Junior Agents (Haiku Models)               │
    │                   Specialized Developers                    │
    └──────────────────────────────────────────────────────────────┘
```

---

## Orchestrator Agent (Claude Sonnet Model)

### **project-orchestrator** - Development Phase Coordinator
**Model Type:** Claude Sonnet (for strategic thinking and complex coordination)

**Primary Responsibilities:**
- Analyze project specifications from `/specs/` directory to understand requirements
- Break down development into executable phases based on tasks.md
- Coordinate phase transitions (Setup → Testing → Implementation → Integration → Polish)
- Provide clear, actionable guidance to each Tech Lead for their domain
- Clarify technical doubts and resolve ambiguities for Tech Leads
- Monitor overall project progress and identify bottlenecks
- Ensure alignment between different Tech Lead teams
- Validate that each phase meets acceptance criteria before proceeding

**Key Coordination Activities:**
1. **Phase Planning**: Review specs and tasks.md to create phase execution plans
2. **Task Distribution**: Assign task groups to appropriate Tech Leads based on expertise
3. **Dependency Management**: Ensure dependent tasks are completed in correct order
4. **Conflict Resolution**: Mediate between Tech Leads when integration issues arise
5. **Quality Gates**: Verify phase completion before authorizing next phase

**Communication Protocols:**
- **With CTO**: Status reports, phase completion notifications, escalation of critical issues
- **With Think-Tank**: Consult on strategic decisions, alternative approaches, repeated failures
- **With Tech Leads**: Clear task assignments, requirement clarifications, progress reviews

**Phase Orchestration Workflow:**
```
1. Analyze current phase requirements from specs/
2. Identify required Tech Leads for phase
3. Create detailed phase execution plan
4. Brief Tech Leads with clear objectives
5. Monitor execution and provide guidance
6. Validate phase completion criteria
7. Authorize transition to next phase
```

**Decision Authority:**
- Can adjust task priorities within phases
- Can reassign tasks between Tech Leads
- Can request Think-Tank consultation for strategic decisions
- Cannot modify project requirements without CTO approval
- Cannot skip TDD principles or quality gates

### Phase-Specific Orchestration Examples

#### Phase 3.1: Setup (T001-T007)
**Orchestrator Actions:**
1. Brief devops-architect on environment setup requirements
2. Coordinate parallel execution of T003-T007 after T001-T002
3. Ensure UV package manager compliance across all setup tasks
4. Validate DuckDB initialization with backend-architect

**Tech Leads Involved:** devops-architect, backend-architect

#### Phase 3.2: Tests First (T008-T022)
**Orchestrator Actions:**
1. Brief test-architect on TDD requirements (tests must fail first)
2. Distribute contract tests (T008-T017) to contract-tester team
3. Assign integration tests (T018-T022) for parallel execution
4. Enforce RED phase before any implementation begins
5. Consult Think-Tank if tests aren't properly isolated

**Tech Leads Involved:** test-architect (primary), all others for test review

#### Phase 3.3: Core Implementation (T023-T048)
**Orchestrator Actions:**
1. Coordinate model creation with backend-architect (T023-T029)
2. Oversee service development with email-processing-lead (T030-T036)
3. Guide API implementation with api-architect (T037-T045)
4. Monitor CLI development progress (T046-T048)
5. Ensure dependencies between services and endpoints are respected
6. Request Think-Tank consultation for architectural decisions

**Tech Leads Involved:** All tech leads actively implementing

#### Phase 3.4: Integration (T049-T053)
**Orchestrator Actions:**
1. Facilitate cross-team integration meetings
2. Coordinate database connection pooling with backend-architect
3. Oversee logging infrastructure with devops-architect
4. Ensure git workflow compliance (YYYY-MM-DD-HH-MM-SS branches)
5. Resolve integration conflicts between teams

**Tech Leads Involved:** backend-architect, devops-architect, email-processing-lead

#### Phase 3.5: Polish (T054-T062)
**Orchestrator Actions:**
1. Coordinate final testing with test-architect
2. Monitor performance benchmarks (100 emails/minute)
3. Review documentation updates
4. Facilitate code cleanup and refactoring
5. Validate all acceptance criteria met
6. Prepare phase completion report for CTO

**Tech Leads Involved:** test-architect, api-architect, backend-architect

---

## Think-Tank Advisory Group (Claude Sonnet Models)

### Purpose
The Think-Tank serves as a strategic advisory body to the Orchestrator, providing alternative perspectives, identifying patterns of inefficiency, and suggesting course corrections when the project encounters obstacles.

### Members

#### 1. **strategy-advisor** - Strategic Planning Specialist
**Focus:** Long-term project vision and architectural decisions
**Advises on:**
- Alternative architectural approaches
- Technology stack optimizations
- Risk mitigation strategies
- Resource allocation efficiency

#### 2. **pattern-analyst** - Pattern Recognition Specialist
**Focus:** Identifying recurring issues and systemic problems
**Advises on:**
- Detecting repeated error patterns
- Identifying inefficient workflows
- Suggesting process improvements
- Recognizing team communication breakdowns

#### 3. **quality-auditor** - Quality Assurance Strategist
**Focus:** Maintaining code quality and testing standards
**Advises on:**
- Test coverage gaps
- Technical debt accumulation
- Performance bottlenecks
- Security vulnerabilities

### Think-Tank Operating Principles

**Activation Triggers:**
1. Orchestrator explicitly requests consultation
2. Same error occurs 3+ times across different teams
3. Phase deadline at risk (>20% behind schedule)
4. Tech Leads report conflicting approaches
5. Integration failures between multiple components

**Advisory Process:**
```
1. Receive consultation request from Orchestrator
2. Analyze problem context and history
3. Each member provides perspective from their specialty
4. Collaborate to form consensus recommendation
5. Present alternatives with pros/cons to Orchestrator
6. Document decision rationale for future reference
```

**Advisory Scope:**
- **CAN**: Suggest alternative approaches, identify risks, recommend process changes
- **CANNOT**: Override Orchestrator decisions, directly instruct Tech Leads, modify code

**Consultation Examples:**

1. **Repeated Test Failures**
   - Pattern-analyst identifies common failure cause
   - Strategy-advisor suggests architectural adjustment
   - Quality-auditor recommends additional test coverage

2. **Performance Issues**
   - Quality-auditor identifies bottleneck location
   - Strategy-advisor proposes optimization strategies
   - Pattern-analyst checks for similar issues elsewhere

3. **Integration Conflicts**
   - Strategy-advisor reviews system boundaries
   - Pattern-analyst identifies communication gaps
   - Quality-auditor suggests integration test improvements

---

## Orchestrator-Think-Tank Interaction Protocol

### Regular Consultations
- **Weekly Review**: Orchestrator presents progress and challenges
- **Phase Transitions**: Think-Tank reviews phase completion metrics
- **Architecture Decisions**: Major technical choices require advisory input

### Emergency Consultations
- **Critical Failures**: System-wide issues affecting multiple teams
- **Deadline Risks**: When phase completion is jeopardized
- **Technical Debates**: When Tech Leads cannot reach consensus

### Communication Format
```yaml
consultation_request:
  from: project-orchestrator
  to: think-tank
  issue: "Description of problem"
  context: "Current phase, affected teams, attempted solutions"
  urgency: "critical|high|normal|low"
  
advisory_response:
  from: think-tank
  to: project-orchestrator
  recommendations:
    - option_1: "Description with pros/cons"
    - option_2: "Alternative approach with trade-offs"
  consensus: "Preferred recommendation"
  rationale: "Reasoning behind recommendation"
```

---

## Senior Developer Agents (Claude Sonnet Models)

### 1. **backend-architect** - Backend Architecture Lead
**Responsibilities:**
- Design system architecture and data flow
- Review database schemas and API contracts
- Delegate backend implementation tasks to junior agents
- Ensure scalability and performance requirements
- Code review and integration validation

**Delegates to:** model-builder, service-developer, api-developer, database-engineer

**Key Tasks Ownership:** T001, T007, T023-T029, T030-T036, T049

---

### 2. **test-architect** - Test Strategy Lead
**Responsibilities:**
- Design test strategy and coverage requirements
- Ensure TDD principles are followed (RED-GREEN-Refactor)
- Review test implementations for completeness
- Coordinate contract, integration, and unit testing
- Validate test independence and parallelization

**Delegates to:** contract-tester, integration-tester, unit-tester, performance-tester

**Key Tasks Ownership:** T005, T008-T022, T054-T058, T061

---

### 3. **devops-architect** - DevOps & Infrastructure Lead
**Responsibilities:**
- Design deployment and CI/CD pipelines
- Configure development environments
- Manage git workflow and branching strategy
- Oversee dependency management with UV
- Ensure proper logging and monitoring

**Delegates to:** setup-engineer, git-specialist, dependency-manager, logger-specialist

**Key Tasks Ownership:** T002-T004, T006, T050, T052, T053

---

### 4. **email-processing-lead** - Email Processing Domain Expert
**Responsibilities:**
- Architect email parsing and thread management
- Design compression and reconstruction strategies
- Oversee quarantine and error handling flows
- Validate email metadata preservation
- Ensure thread relationship integrity

**Delegates to:** email-parser-dev, compression-specialist, thread-manager-dev

**Key Tasks Ownership:** T030, T035-T040, T051

---

### 5. **api-architect** - API Design Lead
**Responsibilities:**
- Design RESTful API architecture
- Review endpoint implementations
- Ensure API consistency and standards
- Coordinate with frontend requirements
- Manage API documentation

**Delegates to:** api-developer, endpoint-specialist, middleware-developer

**Key Tasks Ownership:** T037-T045, T052, T060

---

## Junior Developer Agents (Claude Haiku Models)

### Backend Development Team

#### 1. **model-builder** - Data Model Developer
**Specialization:** Creating Pydantic/SQLAlchemy models
**Tasks:** T023-T029 (Device, MeterReading, EmailMessage, EmailThread, CompressedEmail, Report, ProcessingLog models)
**Reports to:** backend-architect

---

#### 2. **service-developer** - Business Logic Developer
**Specialization:** Implementing service layer components
**Tasks:** T031-T034 (DeviceExtractor, PDFConverter, FolderManager, ArchiveManager services)
**Reports to:** backend-architect

---

#### 3. **database-engineer** - Database Specialist
**Specialization:** DuckDB operations and optimization
**Tasks:** T007, T034, T049 (Schema creation, ArchiveManager, connection pooling)
**Reports to:** backend-architect

---

### Testing Team

#### 4. **contract-tester** - Contract Test Developer
**Specialization:** API contract testing with pytest
**Tasks:** T008-T017 (All contract tests for endpoints)
**Reports to:** test-architect

---

#### 5. **integration-tester** - Integration Test Developer
**Specialization:** End-to-end flow testing
**Tasks:** T018-T022 (Email processing, duplicate handling, quarantine, thread reconstruction, compression flows)
**Reports to:** test-architect

---

#### 6. **unit-tester** - Unit Test Developer
**Specialization:** Component-level testing
**Tasks:** T054-T056 (Unit tests for extractors, parsers, compression)
**Reports to:** test-architect

---

#### 7. **performance-tester** - Performance Test Developer
**Specialization:** Load and performance testing
**Tasks:** T057-T058 (100 emails/minute, <3 second processing)
**Reports to:** test-architect

---

### Email Processing Team

#### 8. **email-parser-dev** - Email Parser Developer
**Specialization:** .eml file parsing and metadata extraction
**Tasks:** T030, T025 (EmailParser service, EmailMessage model)
**Reports to:** email-processing-lead

---

#### 9. **compression-specialist** - Compression Developer
**Specialization:** Email compression algorithms (zstd, gzip)
**Tasks:** T035, T027, T040 (CompressionService, CompressedEmail model, compress endpoint)
**Reports to:** email-processing-lead

---

#### 10. **thread-manager-dev** - Thread Management Developer
**Specialization:** Email thread tracking and reconstruction
**Tasks:** T036, T026, T038-T039 (ThreadManager, EmailThread model, thread endpoints)
**Reports to:** email-processing-lead

---

### API Development Team

#### 11. **api-developer** - REST API Developer
**Specialization:** FastAPI endpoint implementation
**Tasks:** T037, T041-T045 (Main API endpoints)
**Reports to:** api-architect

---

#### 12. **endpoint-specialist** - Endpoint Optimization Developer
**Specialization:** API response optimization and caching
**Tasks:** T042-T044 (Device readings, reports, dashboard endpoints)
**Reports to:** api-architect

---

#### 13. **middleware-developer** - Middleware Developer
**Specialization:** FastAPI middleware and request handling
**Tasks:** T052 (CORS, request logging, authentication middleware)
**Reports to:** api-architect

---

### Infrastructure Team

#### 14. **setup-engineer** - Environment Setup Developer
**Specialization:** Project structure and initial configuration
**Tasks:** T001, T005-T006 (Project structure, pytest config, formatting tools)
**Reports to:** devops-architect

---

#### 15. **dependency-manager** - Dependency Management Specialist
**Specialization:** UV package management
**Tasks:** T002-T004 (UV environment, core and dev dependencies)
**Reports to:** devops-architect

---

#### 16. **git-specialist** - Git Workflow Developer
**Specialization:** Git branching and automation
**Tasks:** T053 (YYYY-MM-DD-HH-MM-SS branch creation)
**Reports to:** devops-architect

---

#### 17. **logger-specialist** - Logging Infrastructure Developer
**Specialization:** Structured logging and monitoring
**Tasks:** T050-T051 (JSON logging, error context, quarantine workflow)
**Reports to:** devops-architect

---

### CLI Development Team

#### 18. **cli-developer** - CLI Command Developer
**Specialization:** Click/Typer CLI implementation
**Tasks:** T046-T048 (meter-cli process, validate, report commands)
**Reports to:** backend-architect

---

### Documentation Team

#### 19. **doc-writer** - Documentation Specialist
**Specialization:** Technical documentation and API docs
**Tasks:** T059-T060 (Update CLAUDE.md, create API documentation)
**Reports to:** api-architect

---

#### 20. **cleanup-specialist** - Code Quality Developer
**Specialization:** Refactoring and code optimization
**Tasks:** T062 (Cleanup and refactor duplicated code)
**Reports to:** backend-architect

---

## Delegation Workflow

### 1. Strategic Planning Phase
```
CTO → Orchestrator (← Think-Tank advises) → Phase Execution Plan
```
- CTO provides project objectives and priorities
- Orchestrator analyzes specs/ and tasks.md to understand requirements
- Think-Tank consulted for strategic decisions and risk assessment
- Orchestrator creates detailed phase execution plan

### 2. Task Assignment Phase
```
Orchestrator → Senior Tech Leads → Junior Developer(s)
```
- Orchestrator briefs Tech Leads on phase objectives and task groups
- Orchestrator clarifies requirements and resolves ambiguities
- Senior Tech Leads create implementation plans for their domains
- Senior Tech Leads delegate specific tasks to appropriate Junior Developers

### 3. Implementation Phase
```
Junior Developer → Implementation → Senior Tech Lead Review → Orchestrator Validation
```
- Junior Developers implement assigned tasks
- Submit code for review to their Senior Tech Lead
- Senior Tech Lead validates implementation meets requirements
- Orchestrator confirms phase milestones are being met

### 4. Integration Phase
```
Orchestrator → Senior Tech Lead Coordination → Integration
```
- Orchestrator facilitates cross-team coordination meetings
- Senior Tech Leads resolve integration dependencies
- Orchestrator monitors integration progress and addresses blockers
- Think-Tank consulted if integration conflicts arise

### 5. Quality Assurance Phase
```
test-architect → Testing Teams → Orchestrator → Phase Completion
```
- test-architect ensures all tests pass
- Performance requirements are met
- Documentation is complete

---

## Communication Protocols

### Orchestrator-to-CTO Communication
- Phase completion reports with metrics
- Critical issue escalations requiring executive decision
- Resource constraint notifications
- Project timeline updates and adjustments

### Orchestrator-to-Think-Tank Communication
- Strategic consultation requests
- Pattern analysis for recurring issues
- Alternative approach evaluations
- Risk assessment for major decisions

### Orchestrator-to-Senior Communication
- Phase kickoff briefings with clear objectives
- Task group assignments with dependencies
- Requirement clarifications and ambiguity resolution
- Progress checkpoints and milestone reviews
- Cross-team coordination facilitation

### Senior-to-Orchestrator Communication
- Task completion status updates
- Technical blocker escalations
- Integration conflict reports
- Resource requirement requests
- Clarification needs on specifications

### Senior-to-Senior Communication
- Architecture decisions requiring consensus
- Cross-domain integration points
- Resource allocation and priority changes
- Blocking issues requiring escalation

### Senior-to-Junior Communication
- Clear task specifications with acceptance criteria
- Code review feedback with specific improvements
- Technical guidance and best practices
- Progress monitoring and deadline management

### Junior-to-Senior Communication
- Task completion notifications
- Clarification requests on requirements
- Blocking issue escalation
- Code review requests

---

## Parallel Execution Groups

### Group A: Setup Team (T001-T007)
- setup-engineer + dependency-manager + database-engineer
- Can work in parallel after T001-T002

### Group B: Testing Team (T008-T022)
- contract-tester + integration-tester
- All tests can be written in parallel

### Group C: Model Team (T023-T029)
- model-builder
- All models can be created in parallel

### Group D: Service Team (T030-T036)
- service-developer + email-parser-dev + compression-specialist + thread-manager-dev
- Services depend on models but can parallelize among themselves

### Group E: API Team (T037-T045)
- api-developer + endpoint-specialist
- Endpoints depend on services but can parallelize endpoint creation

---

## Success Metrics

### For Senior Agents
- Architecture decisions align with requirements
- Junior developers complete tasks within estimates
- Integration points work seamlessly
- Code quality standards maintained

### For Junior Agents
- Tasks completed according to specifications
- Code passes review on first or second attempt
- Tests written before implementation (TDD)
- Documentation included with code

---

## Escalation Path

1. **Technical Issues**: Junior → Senior Tech Lead → Orchestrator → Think-Tank/CTO
2. **Test Failures**: Junior → test-architect → Orchestrator → CTO
3. **Integration Problems**: Senior Tech Lead → Orchestrator → Think-Tank consultation → CTO
4. **Performance Issues**: performance-tester → test-architect → Orchestrator → Think-Tank → CTO
5. **Phase Delays**: Senior Tech Lead → Orchestrator → Think-Tank analysis → CTO
6. **Repeated Errors**: Senior Tech Lead → Orchestrator → Think-Tank (pattern-analyst) → Solution
7. **Security Concerns**: Any Agent → devops-architect → Orchestrator → CTO (immediate escalation)
8. **Strategic Decisions**: Orchestrator → Think-Tank consultation → CTO approval

---

## Agent Invocation Examples

### Orchestrator Invocation
```bash
# Invoke orchestrator for phase planning
claude-agent project-orchestrator \
  --model sonnet \
  --task "Plan and coordinate Phase 3.2: Tests First" \
  --context "@specs/002-claude-md-project/tasks.md" \
  --phase "3.2" \
  --tech-leads "test-architect,backend-architect,api-architect"
```

### Think-Tank Consultation
```bash
# Request think-tank advisory on repeated failures
claude-agent think-tank \
  --model sonnet \
  --members "strategy-advisor,pattern-analyst,quality-auditor" \
  --issue "Contract tests failing repeatedly across multiple teams" \
  --context "@logs/test-failures.log" \
  --urgency "high"
```

### Orchestrator with Think-Tank Support
```bash
# Orchestrator requesting strategic consultation
claude-agent project-orchestrator \
  --model sonnet \
  --task "Evaluate alternative approaches for email compression" \
  --consult think-tank \
  --context "@specs/002-claude-md-project/research.md" \
  --decision-required "compression-strategy"
```

### Senior Agent Invocation (via Orchestrator delegation)
```bash
# Invoke backend-architect for system design
claude-agent backend-architect \
  --model sonnet \
  --task "Design service architecture for email processing" \
  --context "@specs/002-claude-md-project/plan.md" \
  --delegated-by "project-orchestrator" \
  --phase "3.3"
```

### Junior Agent Invocation (via Senior delegation)
```bash
# Invoke model-builder for creating Device model
claude-agent model-builder \
  --model haiku \
  --task "T023: Create Device model" \
  --spec "@specs/002-claude-md-project/data-model.md" \
  --supervisor backend-architect \
  --phase "3.3"
```

### Parallel Team Invocation (coordinated by Orchestrator)
```bash
# Launch all contract testers in parallel
for task in T008 T009 T010 T011 T012; do
  claude-agent contract-tester \
    --model haiku \
    --task "$task" \
    --spec "@contracts/api-spec.yaml" \
    --supervisor test-architect \
    --orchestrated-by "project-orchestrator" \
    --async &
done
```

---

## Notes

- Each agent has a single, well-defined responsibility area
- No overlapping roles between agents
- Clear reporting hierarchy maintained
- Senior agents provide architecture and review
- Junior agents focus on implementation
- All agents follow TDD principles
- UV package manager used exclusively
- Git workflow with timestamped branches enforced

---

*Last Updated: 2025-09-11*
*Version: 1.1.0*
*Changes: Added Orchestrator and Think-Tank Advisory Group for strategic coordination*