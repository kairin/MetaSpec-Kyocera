# Domain-Specific Validation Prompts for Guardian Agents

**Based on**: Git Workflow Implementation Plan Validation (STEP 4)
**Scope**: All Guardian Agent domains (Strategy, Design, Architecture, Development, Infrastructure, Operations)
**Purpose**: Systematic validation framework that adapts to each domain's specific requirements

## **UNIVERSAL VALIDATION FRAMEWORK**

### **Core Validation Categories** (Applied to ALL domains)

1. **Dependency Sequence Validation**
2. **Shared Components Analysis**
3. **Configuration Consistency Check**
4. **Error Handling Patterns Review**
5. **Integration Cross-Reference Validation**
6. **Over-Engineering Detection**
7. **Domain Best Practices Compliance**
8. **Implementation Completeness Audit**
9. **Constitutional Adherence Check**
10. **Final Go/No-Go Assessment**

---

## **1. DEPENDENCY SEQUENCE VALIDATION**

### **Strategy Domain (001-020) Validation Prompt**
```
Audit the strategy agent implementation plan with focus on decision flow architecture:

Review all strategy agent implementations considering:
1. Market research sequence - which analyses must complete first?
2. Stakeholder input dependencies - what decisions require executive approval?
3. Competitive analysis prerequisites - what data feeds strategic decisions?
4. Product roadmap dependencies - how do strategy decisions flow to execution?
5. Risk assessment integration - where do risk factors impact strategy?

For each strategy agent implementation plan, verify:
- Market data sources are accessible and validated
- Decision frameworks are consistent across agents
- Stakeholder communication protocols are defined
- Strategy-to-execution handoff is clear
- Risk mitigation is integrated throughout

Flag any missing dependencies between strategy formulation and execution phases.
```

### **Design Domain (021-040) Validation Prompt**
```
Audit the design agent implementation plan with focus on design system architecture:

Review all design agent implementations considering:
1. User research dependencies - which insights must inform design decisions?
2. Design system component hierarchy - what foundational elements come first?
3. Accessibility requirement integration - how are a11y standards enforced?
4. Cross-platform consistency rules - how do designs adapt across contexts?
5. Usability testing feedback loops - where do test results influence design?

For each design agent implementation plan, verify:
- Design system library is shared and versioned
- User research templates are standardized
- Accessibility guidelines are integrated throughout
- Design-to-development handoff is seamless
- Usability metrics are consistently tracked

Flag any missing connections between user research, design creation, and validation phases.
```

### **Development Domain (061-090) Validation Prompt**
```
Audit the development agent implementation plan with focus on code architecture:

Review all development agent implementations considering:
1. Architecture decision sequence - which technical choices must be made first?
2. Database schema dependencies - how do data models impact application structure?
3. API contract requirements - what interfaces need to be stable?
4. Testing strategy integration - how does TDD flow through development?
5. Security review checkpoints - where are security gates enforced?

For each development agent implementation plan, verify:
- Architecture decisions precede implementation
- Database schemas are designed before application code
- API contracts are defined and tested first
- Code quality standards are enforced consistently
- Security scans pass before deployment

Flag any violations of TDD principles or missing architecture prerequisites.
```

---

## **2. SHARED COMPONENTS ANALYSIS**

### **Universal Shared Components Prompt**
```
Analyze the implementation for shared component opportunities across [DOMAIN] agents:

Map out shared functionality considering:
1. Common data sources and APIs:
   - What external services do multiple agents use?
   - How can API clients be standardized?
   - Where should caching layers be implemented?

2. Reusable business logic:
   - What algorithms or processes are repeated?
   - Which validation rules appear in multiple agents?
   - How can decision frameworks be shared?

3. Standardized communication patterns:
   - What message formats are used between agents?
   - How should error codes be standardized?
   - Where can notification templates be reused?

4. Configuration and constants:
   - What settings should be centralized?
   - Which thresholds and limits are domain-wide?
   - How can environment-specific configs be managed?

For each shared component identified:
- Estimate lines of code saved through reuse
- Identify maintenance benefits
- Assess complexity of extraction
- Plan migration strategy for existing implementations

Recommend whether to refactor now or defer to v2.
```

---

## **3. CONFIGURATION CONSISTENCY CHECK**

### **Domain-Agnostic Configuration Validation**
```
Validate configuration management across [DOMAIN] agents:

CONFIGURATION SCHEMA CONSISTENCY:
☐ All agents use same configuration format (YAML/JSON/ENV)
☐ Configuration keys follow consistent naming convention
☐ Default values are documented and reasonable
☐ Environment-specific overrides are supported
☐ Sensitive data handling is consistent (secrets, API keys)
☐ Configuration validation happens at agent startup

CONFIGURATION LOADING PATTERNS:
☐ Configuration loading code is shared across agents
☐ Error handling for missing/invalid config is uniform
☐ Configuration hot-reloading is supported where needed
☐ Configuration precedence is clearly defined
☐ Multi-environment support (dev/staging/prod) works consistently

DOMAIN-SPECIFIC CONFIGURATIONS:
For Strategy agents: Market data sources, decision thresholds, stakeholder lists
For Design agents: Design system tokens, accessibility standards, device breakpoints
For Development agents: Code quality rules, testing frameworks, deployment targets
For Infrastructure agents: Resource limits, security policies, monitoring configs
For Operations agents: Alert thresholds, backup schedules, incident escalation rules

Check configuration interdependencies and circular references.
```

---

## **4. ERROR HANDLING PATTERNS REVIEW**

### **Universal Error Handling Validation**
```
Review error handling consistency across [DOMAIN] agents:

ERROR CLASSIFICATION:
☐ Consistent error categories (user error, system error, integration error)
☐ Standardized error codes across domain
☐ Error severity levels uniformly applied
☐ Error context includes sufficient debugging information
☐ Error messages are user-friendly and actionable

ERROR RECOVERY PATTERNS:
☐ Retry logic is consistent and reasonable
☐ Circuit breaker patterns implemented for external dependencies
☐ Graceful degradation strategies defined
☐ Rollback procedures documented and tested
☐ Error escalation paths clearly defined

LOGGING AND MONITORING:
☐ Error logging format is standardized
☐ Error tracking integration (e.g., error monitoring service)
☐ Error metrics are collected consistently
☐ Alert thresholds are appropriate for each error type
☐ Error investigation tools are available

DOMAIN-SPECIFIC ERROR SCENARIOS:
Strategy: Market data unavailable, stakeholder approval timeout
Design: Design system component missing, accessibility violation
Development: Build failure, test timeout, deployment error
Infrastructure: Resource exhaustion, security policy violation
Operations: Service degradation, backup failure, incident escalation

Test error handling with chaos engineering principles.
```

---

## **5. INTEGRATION CROSS-REFERENCE VALIDATION**

### **Agent Integration Validation Prompt**
```
Validate cross-references and integration points for [DOMAIN] agents:

INTRA-DOMAIN INTEGRATIONS:
For each agent in [DOMAIN], verify:
- Links to other agents in same domain are valid
- Data flow between agents is clearly defined
- Handoff protocols are documented and tested
- Shared state management is consistent
- Version compatibility is maintained

INTER-DOMAIN INTEGRATIONS:
Check these integration patterns:
1. Strategy → Design: Requirements flow, feedback loops
2. Design → Development: Design system integration, asset handoff
3. Development → Infrastructure: Deployment requirements, resource needs
4. Infrastructure → Operations: Monitoring setup, maintenance procedures
5. Operations → Strategy: Performance data, user feedback

EXTERNAL INTEGRATIONS:
☐ Third-party APIs are consistently integrated
☐ External tool authentication is standardized
☐ Data import/export formats are compatible
☐ Webhook and event handling is uniform
☐ External service failure handling is robust

Report any broken references, version mismatches, or missing integration tests.
```

---

## **6. OVER-ENGINEERING DETECTION**

### **Domain-Specific Over-Engineering Patterns**
```
Review [DOMAIN] agent implementations for over-engineering:

STRATEGY DOMAIN OVER-ENGINEERING:
1. Unnecessary complexity:
   - Complex ML models for simple market analysis
   - Real-time dashboards for monthly planning cycles
   - Advanced forecasting for short-term decisions

2. Premature optimization:
   - Caching for infrequently accessed market data
   - Parallel processing for sequential strategic decisions
   - Complex state machines for linear planning processes

3. Feature creep:
   - Full CRM integration for simple stakeholder management
   - Advanced visualization for internal decision making
   - Multi-tenant support for single-organization use

DESIGN DOMAIN OVER-ENGINEERING:
1. Unnecessary abstraction:
   - Generic design system for specific use cases
   - Complex animation framework for simple interactions
   - Advanced state management for static content

2. Tool overkill:
   - Full design automation for manual creative processes
   - Complex asset pipeline for simple websites
   - Advanced accessibility testing for internal tools

DEVELOPMENT DOMAIN OVER-ENGINEERING:
1. Architecture complexity:
   - Microservices for simple applications
   - Event sourcing for CRUD operations
   - Complex caching for low-traffic applications

2. Technology stack bloat:
   - Multiple frameworks for single-purpose application
   - Complex build pipeline for simple projects
   - Advanced monitoring for development environments

For each over-engineered component:
- Calculate complexity reduction opportunity (lines of code, dependencies)
- Estimate maintenance burden reduction
- Identify features that would be lost
- Recommend simplification approach
```

---

## **7. DOMAIN BEST PRACTICES COMPLIANCE**

### **Strategy Agent Best Practices**
```
Validate strategy agents against industry best practices:

STRATEGIC PLANNING:
☐ Market analysis follows established frameworks (Porter's Five Forces, etc.)
☐ Stakeholder analysis includes all affected parties
☐ Risk assessment is integrated throughout planning process
☐ Strategic options are evaluated against clear criteria
☐ Implementation roadmaps are realistic and resource-aware

DECISION MAKING:
☐ Decision criteria are explicit and consistently applied
☐ Decision rationale is documented for future reference
☐ Stakeholder input is systematically collected and considered
☐ Decision reversibility and exit strategies are planned
☐ Success metrics are defined before implementation

COMMUNICATION:
☐ Strategic communications are clear and actionable
☐ Different audiences receive appropriately tailored messages
☐ Feedback loops exist for strategy refinement
☐ Progress reporting is regular and meaningful
☐ Strategic changes are communicated promptly
```

### **Design Agent Best Practices**
```
Validate design agents against design system best practices:

DESIGN SYSTEM:
☐ Component library follows atomic design principles
☐ Design tokens are used consistently for visual properties
☐ Components are documented with usage guidelines
☐ Accessibility standards (WCAG 2.1 AA) are met
☐ Cross-platform consistency is maintained

USER EXPERIENCE:
☐ User research informs all design decisions
☐ Usability testing validates design solutions
☐ User journeys are mapped and optimized
☐ Error states and edge cases are designed
☐ Performance impact of design decisions is considered

COLLABORATION:
☐ Design-development handoff is smooth and complete
☐ Design rationale is documented for stakeholders
☐ Version control and change management for designs
☐ Design reviews include relevant stakeholders
☐ Design updates are communicated effectively
```

### **Development Agent Best Practices**
```
Validate development agents against software engineering best practices:

CODE QUALITY:
☐ Code follows established style guidelines
☐ Code reviews are thorough and constructive
☐ Technical debt is actively managed
☐ Code coverage meets minimum thresholds
☐ Static analysis tools are integrated and passing

TESTING:
☐ Test-driven development (TDD) is followed
☐ Unit tests cover core business logic
☐ Integration tests validate component interactions
☐ End-to-end tests cover critical user paths
☐ Performance tests validate non-functional requirements

SECURITY:
☐ Security scanning is integrated into CI/CD pipeline
☐ Dependency vulnerabilities are regularly assessed
☐ Input validation and sanitization is comprehensive
☐ Authentication and authorization are properly implemented
☐ Security headers and configurations are applied
```

---

## **8. IMPLEMENTATION COMPLETENESS AUDIT**

### **Universal Completeness Check Template**
```
Verify [DOMAIN] agent implementation covers all required scenarios:

CORE WORKFLOWS:
☐ Happy path scenarios are fully implemented
☐ Alternative workflows are supported
☐ Workflow transitions are smooth and logical
☐ User guidance is provided throughout workflows
☐ Workflow completion is clearly indicated

EDGE CASES:
☐ Boundary conditions are handled appropriately
☐ Invalid input scenarios are gracefully managed
☐ Resource constraints (memory, CPU, network) are handled
☐ Concurrent operation conflicts are resolved
☐ Data inconsistency scenarios are addressed

ERROR SCENARIOS:
☐ Network failures don't cause data loss
☐ Service unavailability has fallback behavior
☐ Partial failures have recovery procedures
☐ User errors provide helpful feedback
☐ System errors are logged and escalated appropriately

INTEGRATION SCENARIOS:
☐ Upstream service changes are handled gracefully
☐ Downstream service failures don't cascade
☐ Cross-domain data consistency is maintained
☐ Version compatibility across integrations
☐ Migration procedures for breaking changes

PERFORMANCE SCENARIOS:
☐ High load conditions are handled appropriately
☐ Resource usage is monitored and limited
☐ Performance degrades gracefully under stress
☐ Caching strategies are effective and correct
☐ Optimization opportunities are identified
```

---

## **9. CONSTITUTIONAL ADHERENCE CHECK**

### **Universal Constitutional Compliance**
```
Verify [DOMAIN] agents follow Guardian Agent constitutional principles:

CORE PRINCIPLES:
☐ Agent specialization is clearly defined and non-overlapping
☐ Model optimization (Haiku vs Sonnet) is appropriate
☐ Automatic chaining triggers work correctly
☐ Performance SLAs are met consistently
☐ Validation framework compliance is maintained

ARCHITECTURAL PATTERNS:
☐ Single responsibility principle is followed
☐ Interface contracts are well-defined
☐ Dependencies are minimized and explicit
☐ State management is consistent across agents
☐ Error boundaries prevent cascade failures

OPERATIONAL REQUIREMENTS:
☐ Agents are independently deployable
☐ Configuration is externalized and manageable
☐ Logging and monitoring are comprehensive
☐ Performance metrics are collected and analyzed
☐ Security requirements are met throughout

DEVELOPMENT PRACTICES:
☐ Test-driven development is followed
☐ Code quality standards are maintained
☐ Documentation is complete and current
☐ Version control practices are consistent
☐ Deployment processes are automated and reliable

USER EXPERIENCE:
☐ Agent interactions are intuitive and helpful
☐ Error messages are actionable and user-friendly
☐ Performance meets user expectations
☐ Reliability is high and consistent
☐ Feedback mechanisms are available and used
```

---

## **10. FINAL GO/NO-GO ASSESSMENT**

### **Universal Go/No-Go Decision Framework**
```
Perform final pre-implementation assessment for [DOMAIN] agents:

TECHNICAL READINESS:
Score (1-5): Technical implementation quality
Score (1-5): Dependency management completeness
Score (1-5): Error handling robustness
Score (1-5): Performance optimization level
Score (1-5): Security posture strength

OPERATIONAL READINESS:
Score (1-5): Monitoring and alerting coverage
Score (1-5): Documentation completeness
Score (1-5): Deployment automation maturity
Score (1-5): Rollback procedure reliability
Score (1-5): Support process readiness

BUSINESS READINESS:
Score (1-5): User value proposition clarity
Score (1-5): Success metrics definition
Score (1-5): Stakeholder buy-in level
Score (1-5): Resource commitment adequacy
Score (1-5): Timeline realism assessment

RISK ASSESSMENT:
Risk Level (Low/Medium/High/Critical): Technical complexity
Risk Level (Low/Medium/High/Critical): Integration complexity
Risk Level (Low/Medium/High/Critical): Performance uncertainty
Risk Level (Low/Medium/High/Critical): Security vulnerabilities
Risk Level (Low/Medium/High/Critical): Operational complexity

DECISION CRITERIA:
- Average score ≥4.0 across all categories = GO
- Any Critical risk = NO-GO (unless mitigated)
- Score 3.0-3.9 = CONDITIONAL GO (with improvement plan)
- Score <3.0 = NO-GO (major improvements needed)

RECOMMENDATION OUTPUT:
Decision: [GO/NO-GO/CONDITIONAL GO]
Primary risks: [List top 3 risks]
Mitigation plan: [Required actions before GO]
Estimated effort: [Time to address issues]
Success probability: [Percentage confidence]
Recommended timeline: [Suggested implementation schedule]
```

---

## **DOMAIN-SPECIFIC CUSTOMIZATION EXAMPLES**

### **Strategy Domain Adaptations**
- Replace "shell script" with "strategic analysis framework"
- Replace "git commands" with "market research APIs"
- Replace "branch naming" with "decision documentation"
- Replace "commit messages" with "stakeholder communications"

### **Design Domain Adaptations**
- Replace "shell script" with "design system component"
- Replace "git commands" with "design tool APIs"
- Replace "branch naming" with "design version management"
- Replace "commit messages" with "design change documentation"

### **Development Domain Adaptations**
- Keep technical focus but broaden beyond Git workflow
- Include code quality, testing, deployment considerations
- Add security scanning, dependency management
- Include performance optimization, monitoring

This universal framework ensures consistent, thorough validation across all Guardian Agent domains while adapting to each domain's specific requirements and best practices.
