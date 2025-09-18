# Kyocera Agent Team Structure - GitHub-Compatible Mermaid Diagrams

## 1. Overall Team Hierarchy

```mermaid
graph TD
    CTO[CTO - Chief Technical Officer<br/>Human Leader]
    
    CTO --> ORCH[000-project-orchestrator<br/>Sonnet - Phase Coordinator]
    CTO --> TT[Think-Tank Advisory Group]
    
    TT --> SA[001-strategy-advisor<br/>Sonnet]
    TT --> PA[002-pattern-analyst<br/>Sonnet]
    TT --> QA[003-quality-auditor<br/>Sonnet]
    
    ORCH -.->|consults| TT
    
    ORCH --> DA[004-devops-architect<br/>Sonnet]
    ORCH --> TA[005-test-architect<br/>Sonnet]
    ORCH --> BA[006-backend-architect<br/>Sonnet]
    ORCH --> EPL[007-email-processing-lead<br/>Sonnet]
    ORCH --> AA[008-api-architect<br/>Sonnet]
    
    DA --> InfraTeam[Infrastructure Team<br/>009-011 Haiku]
    TA --> TestTeam[Testing Team<br/>012-015 Haiku]
    BA --> BackendTeam[Backend Team<br/>016-018 Haiku]
    EPL --> EmailTeam[Email Processing Team<br/>019-021 Haiku]
    AA --> APITeam[API Team<br/>022-024 Haiku]
    
    DA --> SupportTeam[Support Team<br/>025-026 Haiku]
    AA --> DocTeam[Documentation Team<br/>027-028 Haiku]
```

## 2. Development Phase Workflow

```mermaid
flowchart LR
    Start([Project Start]) --> P31[Phase 3.1: Setup<br/>T001-T007]
    P31 --> P32[Phase 3.2: Tests First<br/>T008-T022]
    P32 --> P33[Phase 3.3: Core Implementation<br/>T023-T048]
    P33 --> P34[Phase 3.4: Integration<br/>T049-T053]
    P34 --> P35[Phase 3.5: Polish<br/>T054-T062]
    P35 --> End([Project Complete])
    
    P31 -.-> Setup[Environment Setup<br/>UV Dependencies<br/>DuckDB Schema<br/>Project Structure]
    P32 -.-> Tests[Contract Tests<br/>Integration Tests<br/>TDD Implementation<br/>Test Infrastructure]
    P33 -.-> Core[Data Models<br/>Services<br/>API Endpoints<br/>CLI Commands]
    P34 -.-> Integration[Database Pooling<br/>Logging Setup<br/>Git Workflow<br/>Cross-team Integration]
    P35 -.-> Polish[Final Testing<br/>Documentation<br/>Performance Validation<br/>Code Cleanup]
```

## 3. Orchestrator Coordination Workflow

```mermaid
flowchart TD
    Start([Phase Start]) --> Analyze[Orchestrator Analyzes<br/>specs/ and tasks.md]
    Analyze --> Plan[Create Phase<br/>Execution Plan]
    Plan --> Brief[Brief Tech Leads<br/>with Clear Objectives]
    Brief --> Monitor[Monitor Execution<br/>& Provide Guidance]
    Monitor --> Check{Phase Complete?}
    Check -->|No| Support[Provide Support<br/>& Resolve Blockers]
    Support --> Monitor
    Check -->|Yes| Validate[Validate Phase<br/>Completion Criteria]
    Validate --> Next[Authorize Transition<br/>to Next Phase]
    Next --> End([Phase Complete])
    
    Plan -.->|Strategic Decisions| Consult[Consult Think-Tank]
    Support -.->|Critical Issues| Consult
    Consult -.-> Plan
    Consult -.-> Support
    
    Support -.->|Critical Issues| Escalate[Escalate to CTO]
```

## 4. Think-Tank Advisory Process

```mermaid
sequenceDiagram
    participant O as 000-project-orchestrator
    participant SA as 001-strategy-advisor
    participant PA as 002-pattern-analyst
    participant QA as 003-quality-auditor
    participant CTO as CTO
    
    Note over O,QA: Think-Tank Consultation Process
    
    O->>SA: Request consultation
    O->>PA: Share problem context
    O->>QA: Provide failure history
    
    Note over SA,QA: Independent Analysis
    SA->>SA: Analyze strategic options
    PA->>PA: Identify patterns
    QA->>QA: Assess quality impact
    
    Note over SA,QA: Collaborative Discussion
    SA->>PA: Share strategic perspective
    PA->>QA: Discuss pattern findings
    QA->>SA: Quality concerns feedback
    
    Note over SA,QA: Consensus Building
    SA->>O: Recommend Option A
    PA->>O: Support with pattern data
    QA->>O: Quality validation
    
    alt Critical Decision
        O->>CTO: Escalate with recommendations
        CTO->>O: Executive decision
    else Normal Decision
        O->>O: Implement recommendation
    end
```

## 5. Delegation Workflow

```mermaid
flowchart TD
    CTO[CTO] --> ORCH[000-project-orchestrator]
    
    ORCH --> PhaseAnalysis[Analyze Current Phase<br/>from specs/]
    PhaseAnalysis --> TechLeadBrief[Brief Senior Tech Leads<br/>with Task Groups]
    
    TechLeadBrief --> DA[004-devops-architect]
    TechLeadBrief --> TA[005-test-architect] 
    TechLeadBrief --> BA[006-backend-architect]
    TechLeadBrief --> EPL[007-email-processing-lead]
    TechLeadBrief --> AA[008-api-architect]
    
    DA --> SE[009-setup-engineer]
    DA --> DM[010-dependency-manager]
    DA --> DE[011-database-engineer]
    
    TA --> CT[012-contract-tester]
    TA --> IT[013-integration-tester]
    TA --> UT[014-unit-tester]
    TA --> PT[015-performance-tester]
    
    BA --> MB[016-model-builder]
    BA --> SD[017-service-developer]
    BA --> CD[018-cli-developer]
    
    EPL --> EPD[019-email-parser-dev]
    EPL --> CS[020-compression-specialist]
    EPL --> TMD[021-thread-manager-dev]
    
    AA --> AD[022-api-developer]
    AA --> ES[023-endpoint-specialist]
    AA --> MD[024-middleware-developer]
    
    SE --> Review1[Code Review by<br/>devops-architect]
    CT --> Review2[Code Review by<br/>test-architect]
    MB --> Review3[Code Review by<br/>backend-architect]
    
    Review1 --> Validation[Orchestrator Validation]
    Review2 --> Validation
    Review3 --> Validation
```

## 6. Communication Protocol Matrix

```mermaid
flowchart LR
    subgraph Levels [Communication Levels]
        CTO[CTO<br/>Human Leader]
        ORCH[000-project-orchestrator<br/>Coordinator]
        TT[Think-Tank<br/>001-003]
        SL[Senior Leads<br/>004-008]
        JD[Junior Devs<br/>009-028]
    end
    
    CTO <-->|Status Reports<br/>Critical Escalations| ORCH
    ORCH <-->|Strategic Consultation<br/>Pattern Analysis| TT
    ORCH <-->|Phase Briefings<br/>Task Assignments| SL
    SL <-->|Task Specifications<br/>Code Reviews| JD
    SL <-->|Architecture Decisions<br/>Integration Points| SL
```

## 7. Parallel Execution Timeline

```mermaid
flowchart LR
    subgraph Phase1 [Phase 3.1: Setup]
        T1[T001-T002<br/>Sequential] --> T2[T003-T007<br/>Parallel]
    end
    
    subgraph Phase2 [Phase 3.2: Testing]
        T3[T008-T017<br/>Contract Tests<br/>Parallel]
        T4[T018-T022<br/>Integration Tests<br/>Parallel]
    end
    
    subgraph Phase3 [Phase 3.3: Implementation]
        T5[T023-T029<br/>Models<br/>Parallel]
        T6[T030-T036<br/>Services<br/>Parallel]
        T7[T037-T045<br/>APIs<br/>Parallel]
        T8[T046-T048<br/>CLI<br/>Parallel]
    end
    
    subgraph Phase4 [Phase 3.4: Integration]
        T9[T049<br/>DB Pool]
        T10[T050-T051<br/>Logging]
        T11[T053<br/>Git Workflow]
    end
    
    subgraph Phase5 [Phase 3.5: Polish]
        T12[T054-T058<br/>Final Tests]
        T13[T059-T060<br/>Documentation]
        T14[T062<br/>Cleanup]
    end
    
    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4
    Phase4 --> Phase5
```

## 8. Task-to-Agent Mapping - Setup Phase

```mermaid
flowchart LR
    subgraph Setup [Phase 3.1: Setup Tasks]
        T001[T001: Project Structure]
        T002[T002: UV Environment]
        T003[T003: Core Dependencies]
        T004[T004: Dev Dependencies]
        T005[T005: Pytest Config]
        T006[T006: Formatting Tools]
        T007[T007: DuckDB Schema]
    end
    
    subgraph Agents [Assigned Agents]
        SE[009-setup-engineer<br/>Haiku]
        DM[010-dependency-manager<br/>Haiku]
        DE[011-database-engineer<br/>Haiku]
    end
    
    T001 --> SE
    T005 --> SE
    T006 --> SE
    T002 --> DM
    T003 --> DM
    T004 --> DM
    T007 --> DE
```

## 9. Task-to-Agent Mapping - Implementation Phase

```mermaid
flowchart LR
    subgraph Implementation [Phase 3.3: Core Implementation]
        T023[T023-T029: Models]
        T030[T030-T034: Services]
        T035[T035-T036: Email Processing]
        T037[T037-T045: API Endpoints]
        T046[T046-T048: CLI Commands]
    end
    
    subgraph Teams [Development Teams]
        MB[016-model-builder<br/>Haiku]
        SD[017-service-developer<br/>Haiku]
        EPD[019-email-parser-dev<br/>Haiku]
        AD[022-api-developer<br/>Haiku]
        CD[018-cli-developer<br/>Haiku]
    end
    
    T023 --> MB
    T030 --> SD
    T035 --> EPD
    T037 --> AD
    T046 --> CD
```

## 10. Escalation Path Workflow

```mermaid
flowchart TD
    Issue[Issue Identified] --> Type{Issue Type?}
    
    Type -->|Technical| Tech[Junior Agent]
    Type -->|Integration| Integration[Senior Tech Lead]
    Type -->|Performance| Perf[performance-tester]
    Type -->|Security| Security[devops-architect]
    Type -->|Repeated Error| Repeat[Senior Tech Lead]
    
    Tech --> SeniorReview[Senior Tech Lead Review]
    SeniorReview --> Resolved1{Resolved?}
    Resolved1 -->|Yes| End1[Issue Resolved]
    Resolved1 -->|No| OrchEscalate[Escalate to Orchestrator]
    
    Integration --> OrchEscalate
    Perf --> TestArch[test-architect]
    TestArch --> OrchEscalate
    Security --> OrchEscalate
    Repeat --> OrchEscalate
    
    OrchEscalate --> OrchReview[Orchestrator Review]
    OrchReview --> Resolved2{Can Orchestrator Resolve?}
    
    Resolved2 -->|Yes| End2[Issue Resolved]
    Resolved2 -->|No| Critical{Critical Issue?}
    
    Critical -->|No| ThinkTank[Think-Tank Consultation]
    Critical -->|Yes| CTOEscalate[Immediate CTO Escalation]
    
    ThinkTank --> Advisory[Advisory Recommendation]
    Advisory --> Implement[Implement Solution]
    Implement --> End3[Issue Resolved]
    
    CTOEscalate --> CTODecision[CTO Decision]
    CTODecision --> End4[Issue Resolved]
```

## 11. Agent Invocation Sequence

```mermaid
sequenceDiagram
    participant CTO as CTO
    participant ORCH as 000-project-orchestrator
    participant TT as Think-Tank
    participant SL as Senior Lead
    participant JD as Junior Dev
    
    Note over CTO,JD: Phase Execution Sequence
    
    CTO->>ORCH: Initialize Phase
    ORCH->>ORCH: Analyze specs/ and tasks.md
    
    alt Strategic Decision Needed
        ORCH->>TT: Request consultation
        TT->>TT: Analyze and discuss
        TT->>ORCH: Provide recommendations
    end
    
    ORCH->>SL: Brief with phase objectives
    ORCH->>SL: Assign task groups
    
    SL->>SL: Create implementation plan
    SL->>JD: Delegate specific tasks
    SL->>JD: Provide technical guidance
    
    loop Task Implementation
        JD->>JD: Implement task
        JD->>SL: Submit for review
        SL->>SL: Code review
        
        alt Review Failed
            SL->>JD: Request improvements
        else Review Passed
            SL->>ORCH: Task completion
        end
    end
    
    ORCH->>ORCH: Validate phase completion
    ORCH->>CTO: Phase completion report
    
    alt Phase Incomplete
        CTO->>ORCH: Request status update
        ORCH->>TT: Consult on delays
    else Phase Complete
        CTO->>ORCH: Authorize next phase
    end
```

## 12. Agent Capability Matrix by Model Type

```mermaid
flowchart TB
    subgraph Sonnet [Sonnet Models - Strategic Thinking]
        ORCH[000-project-orchestrator<br/>Phase coordination<br/>Complex decision making<br/>Cross-team integration]
        TT_Group[001-003 Think-Tank<br/>Strategic analysis<br/>Pattern recognition<br/>Quality assessment]
        SL_Group[004-008 Senior Leads<br/>Architecture design<br/>Code review<br/>Technical leadership]
    end
    
    subgraph Haiku [Haiku Models - Implementation]
        Setup_Team[009-011 Infrastructure<br/>Environment setup<br/>Dependencies<br/>Database config]
        Test_Team[012-015 Testing<br/>Contract tests<br/>Integration tests<br/>Performance tests]
        Dev_Team[016-028 Development<br/>Models, Services, APIs<br/>CLI, Documentation<br/>Code cleanup]
    end
    
    ORCH --> SL_Group
    SL_Group --> Setup_Team
    SL_Group --> Test_Team
    SL_Group --> Dev_Team
    ORCH -.-> TT_Group
```

## 13. Phase-Specific Agent Usage

```mermaid
flowchart LR
    subgraph Phase31 [Phase 3.1: Setup]
        P31_Agents[000, 004, 009-011<br/>Orchestrator<br/>DevOps Architect<br/>Infrastructure Team]
    end
    
    subgraph Phase32 [Phase 3.2: Tests First]
        P32_Agents[000, 005, 012-015<br/>Orchestrator<br/>Test Architect<br/>Testing Team]
    end
    
    subgraph Phase33 [Phase 3.3: Implementation]
        P33_Agents[000, 006-008, 016-024<br/>Orchestrator<br/>All Senior Leads<br/>All Dev Teams]
    end
    
    subgraph Phase34 [Phase 3.4: Integration]
        P34_Agents[000, 004, 006-007, 025-026<br/>Orchestrator<br/>DevOps + Backend<br/>Support Team]
    end
    
    subgraph Phase35 [Phase 3.5: Polish]
        P35_Agents[000, 005, 008, 027-028<br/>Orchestrator<br/>Test + API Leads<br/>Doc Team]
    end
    
    Phase31 --> Phase32
    Phase32 --> Phase33
    Phase33 --> Phase34
    Phase34 --> Phase35
```
