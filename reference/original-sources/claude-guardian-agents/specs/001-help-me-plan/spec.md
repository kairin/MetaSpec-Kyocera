# Feature Specification: Guardian Agent Specialization & Documentation Optimization

**Feature Branch**: `001-help-me-plan`
**Created**: 2025-09-09
**Status**: Draft
**Input**: User description: "help me plan and update each of the md files within this repo to reflect each specific agentic behaviour of a subagent to make it highly specialised. take reference from existing documentation with the goal that each subagent specialisation can lead to optimisation in how we develop apps in general."

**Additional Requirements**: Git workflow agent specialization with model optimization:
- Simple tasks (branch naming, commit formatting) → Haiku models for speed
- Complex decisions (merge strategies, session management) → Sonnet models for reasoning
- Specialized Git workflow agents (101-112) with automatic chaining capabilities

## Execution Flow (main)
```
1. Parse user description from Input
   → Agent specialization enhancement for 40+ Guardian agents
2. Extract key concepts from description
   → Actors: Guardian agents, Claude Code system, developers
   → Actions: Specialize, optimize, update documentation
   → Data: Agent files, relationship mappings, workflow diagrams
   → Constraints: Maintain existing structure, enhance specialization
3. For each unclear aspect:
   → [CLARIFIED]: All reference URLs point to established patterns in this repo
4. Fill User Scenarios & Testing section
   → Developer uses specialized agent for specific task type
5. Generate Functional Requirements
   → Each agent must have unique specialization
   → Documentation must reflect agent capabilities
   → Workflow diagrams must show agent relationships
6. Identify Key Entities
   → Guardian Agent, Specialization Profile, Workflow Chain
7. Run Review Checklist
   → All sections completed with specific requirements
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT specialized behaviors agents need and WHY for development optimization
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for development team stakeholders using Guardian agents

## User Scenarios & Testing *(mandatory)*

### Primary User Story
A development team uses the Guardian Agent system to optimize their application development workflow. Each agent has a highly specialized role that eliminates overlap and maximizes efficiency. When a developer invokes an agent for a specific task, the agent's specialization ensures optimal results and automatic chaining to the next appropriate specialist.

### Acceptance Scenarios
1. **Given** a developer needs strategic product planning, **When** they invoke the strategy guardian agents, **Then** the system automatically chains from high-level strategy (001) through detailed product management (002-006) to design handoff (021)

2. **Given** a developer needs to implement a feature, **When** they start with a development task, **Then** the system routes through architecture validation (041-045) before engaging appropriate development specialists (061-069) with quality assurance (071-073)

3. **Given** a security review is needed, **When** any development agent completes work, **Then** the system automatically engages security operations (092-094) followed by infrastructure deployment (081-083) specialists

4. **Given** a developer views agent documentation, **When** they read any agent file, **Then** they can immediately understand the agent's unique specialization, input requirements, output deliverables, and next-agent chaining logic

### Edge Cases
- What happens when multiple agents have overlapping capabilities? → Clear specialization boundaries prevent conflicts
- How does system handle agent specialization gaps? → Comprehensive coverage across all development lifecycle phases
- What if an agent's specialization changes over time? → Template system allows consistent updates across all agents

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Each Guardian agent MUST have a unique specialization that distinguishes it from all other agents in the system
- **FR-002**: Agent documentation MUST clearly define input sources, processing capabilities, and output destinations with specific examples
- **FR-003**: Agent workflow diagrams MUST visually represent the agent's role in the development pipeline with mermaid flowcharts
- **FR-004**: Agent relationship mappings MUST specify automatic chaining triggers and conditional routing logic
- **FR-005**: Documentation structure MUST follow standardized template for consistency across all 40+ agents
- **FR-006**: Each agent MUST include trigger phrases that enable Claude Code's automatic agent selection and chaining
- **FR-007**: Agent specializations MUST cover the complete software development lifecycle without gaps or overlaps
- **FR-008**: Documentation MUST include practical examples showing how agent specialization optimizes development workflows
- **FR-009**: Agent categories MUST use consistent numbering scheme (001-020: Strategy, 021-040: Design, 041-060: Architecture, 061-080: Development, 081-090: Infrastructure, 091-100: Operations)
- **FR-010**: Each agent file MUST include its position in the workflow chain and next-agent recommendations
- **FR-011**: Git workflow agents (101-112) MUST be optimized for model selection with simple tasks using Haiku models and complex decisions using Sonnet models
- **FR-012**: Agent chaining MUST support conditional routing based on Git workflow type (feature, hotfix, experiment, data pipeline)
- **FR-013**: Branch naming agents MUST generate timestamp-based conventional names automatically
- **FR-014**: Commit message agents MUST enforce structured formatting with temporal tracking
- **FR-015**: Session management agents MUST orchestrate daily Git workflows with morning setup and end-of-day cleanup
- **FR-016**: All 40+ Guardian agents MUST be categorized for optimal model assignment (22 Haiku agents for simple tasks, 28 Sonnet agents for complex reasoning)
- **FR-017**: Junior-level agents (063, 066, 069, 073, 083, 094, 097, 100) MUST use Haiku models for fast execution of routine tasks
- **FR-018**: Leadership and architecture agents (001, 002, 041, 042, 061, 071, 091, 092) MUST use Sonnet models for strategic decisions
- **FR-019**: Agent documentation MUST specify recommended model type based on task complexity and reasoning requirements
- **FR-020**: Workflow chains MUST optimize performance by alternating between Haiku (fast) and Sonnet (reasoning) agents appropriately
- **FR-021**: All Guardian agents MUST include comprehensive validation checklists with ✓/☐/~/✗/⚠️ status tracking
- **FR-022**: Validation framework MUST support multiple perspectives (development, testing, code review, production readiness)
- **FR-023**: Agent validation MUST include automated testing with programmatic pass/fail determination
- **FR-024**: Each agent MUST meet performance SLAs (Haiku <2s, Sonnet <10s) with quantified metrics
- **FR-025**: Validation reports MUST generate in multiple formats (console, JSON, markdown) for different stakeholders
- **FR-026**: Universal validation framework MUST apply 10-step validation process to all Guardian agents regardless of domain
- **FR-027**: Domain-agnostic validation patterns MUST be systematically applied (dependency sequence, shared components, configuration consistency, error handling, integration validation, complexity assessment, best practices, completeness audit, constitutional compliance, go/no-go decision)
- **FR-028**: Each Guardian agent MUST pass domain-specific validation prompts adapted from Git workflow STEP 4 methodology
- **FR-029**: Validation framework MUST detect over-engineering patterns and recommend simplification opportunities
- **FR-030**: Implementation completeness audit MUST cover functional, integration, operational, and documentation completeness

### Key Entities *(include if feature involves data)*
- **Guardian Agent**: A specialized Claude subagent with unique role, capabilities, tools, and chaining behavior
- **Specialization Profile**: Defines agent's unique expertise area, distinguishing it from other agents
- **Workflow Chain**: Sequential and conditional relationships between agents that optimize development processes
- **Agent Category**: Grouping of agents by development lifecycle phase (Strategy, Design, Architecture, Development, Infrastructure, Operations)
- **Trigger Pattern**: Specific phrases and conditions that activate automatic agent selection and chaining
- **Git Workflow Agent**: Specialized agents (101-112) for Git operations with model optimization and temporal tracking
- **Model Optimization Profile**: Assignment of appropriate Claude model (Haiku/Sonnet) based on task complexity
- **Performance Optimization Matrix**: Categorization system that assigns 22 agents to Haiku (junior/routine tasks) and 28 agents to Sonnet (leadership/complex reasoning)
- **Validation Framework**: Comprehensive testing system with multi-perspective validation (✓/☐/~/✗/⚠️) for all agents
- **Performance SLA**: Service level agreements for agent response times and quality metrics
- **Universal Validation Framework**: 10-step validation process applicable to all Guardian agents regardless of domain
- **Domain-Agnostic Validation Patterns**: Systematic validation approach covering dependency sequence, shared components, configuration consistency, error handling, integration validation, complexity assessment, best practices, completeness audit, constitutional compliance, and go/no-go decision making

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed

---
