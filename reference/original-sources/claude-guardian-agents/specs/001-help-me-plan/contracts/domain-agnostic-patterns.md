# Domain-Agnostic Validation Patterns for Guardian Agents

**Purpose**: Universal validation patterns that apply across all Guardian Agent domains
**Based on**: Git Workflow STEP 4 validation methodology
**Scope**: Strategy, Design, Architecture, Development, Infrastructure, Operations

## **PATTERN 1: DEPENDENCY SEQUENCE ANALYSIS**

### **Universal Dependency Pattern**
```
For any Guardian Agent in domain [X]:

PREREQUISITE MAPPING:
1. Input Dependencies: What must exist before this agent can function?
   - Data sources (APIs, databases, files)
   - Configuration requirements
   - Other agent outputs
   - External service availability

2. Processing Dependencies: What order must operations follow?
   - Sequential steps that cannot be parallelized
   - Decision points that affect subsequent processing
   - Validation gates that must pass
   - State changes that affect other operations

3. Output Dependencies: What depends on this agent's outputs?
   - Downstream agents in workflow chains
   - External systems expecting data
   - Human decision makers requiring reports
   - Audit trails and compliance records

VALIDATION CHECKS:
☐ Prerequisites are explicitly documented
☐ Dependency order is enforced programmatically
☐ Missing dependencies trigger clear error messages
☐ Circular dependencies are detected and prevented
☐ Dependency changes are communicated to affected agents
```

### **Domain Application Examples**
- **Strategy**: Market research → competitive analysis → strategic recommendations → execution roadmap
- **Design**: User research → design system → component library → implementation guidelines
- **Development**: Requirements → architecture → implementation → testing → deployment
- **Operations**: Monitoring setup → service deployment → incident procedures → performance optimization

---

## **PATTERN 2: SHARED COMPONENT IDENTIFICATION**

### **Universal Shared Component Pattern**
```
For any Guardian Agent domain [X]:

SHARED FUNCTIONALITY ANALYSIS:
1. Data Processing: What data operations are repeated?
   - Input validation and sanitization
   - Data format conversions
   - Caching and persistence patterns
   - Error handling for data operations

2. Communication Patterns: What interactions are standardized?
   - API client implementations
   - Message queue handling
   - Event publication and subscription
   - Response formatting and status codes

3. Business Logic: What domain rules are consistent?
   - Validation criteria and thresholds
   - Decision trees and business rules
   - Calculation algorithms and formulas
   - Approval and escalation workflows

4. Infrastructure Concerns: What technical patterns repeat?
   - Configuration loading and validation
   - Logging and monitoring integration
   - Security and authentication handling
   - Performance measurement and reporting

REFACTORING OPPORTUNITIES:
☐ Identify code duplication across agents (>3 similar implementations)
☐ Extract common libraries for frequently used patterns
☐ Standardize configuration schemas and loading mechanisms
☐ Create shared utilities for domain-specific operations
☐ Implement common error handling and logging frameworks
```

---

## **PATTERN 3: CONFIGURATION CONSISTENCY FRAMEWORK**

### **Universal Configuration Pattern**
```
For any Guardian Agent domain [X]:

CONFIGURATION SCHEMA:
1. Agent Metadata: Identity and capability information
   - Agent name, version, and description
   - Capability declarations and limitations
   - Performance characteristics and SLAs
   - Contact information and ownership

2. Operational Settings: Runtime behavior configuration
   - Performance tuning parameters
   - Feature flags and toggles
   - Resource limits and timeouts
   - Retry policies and circuit breakers

3. Integration Configuration: External system connections
   - API endpoints and authentication
   - Database connections and credentials
   - Message queue configurations
   - Third-party service integrations

4. Business Configuration: Domain-specific parameters
   - Business rules and validation criteria
   - Workflow routing and decision logic
   - Notification preferences and escalation
   - Compliance and audit requirements

CONSISTENCY VALIDATION:
☐ Configuration format is standardized across domain
☐ Required vs optional settings are clearly marked
☐ Default values are sensible and documented
☐ Environment-specific overrides work correctly
☐ Configuration changes are validated before application
☐ Sensitive data is properly protected and encrypted
```

---

## **PATTERN 4: ERROR HANDLING STANDARDIZATION**

### **Universal Error Handling Pattern**
```
For any Guardian Agent domain [X]:

ERROR CLASSIFICATION HIERARCHY:
1. User Errors: Input validation and usage issues
   - Invalid input parameters or formats
   - Missing required information
   - Authorization and permission issues
   - Rate limiting and quota exceeded

2. System Errors: Technical and infrastructure issues
   - Service unavailability and timeouts
   - Resource exhaustion (memory, disk, CPU)
   - Configuration errors and missing dependencies
   - Network connectivity and communication failures

3. Business Logic Errors: Domain-specific rule violations
   - Workflow state inconsistencies
   - Business rule violations
   - Data integrity and consistency issues
   - Compliance and policy violations

4. Integration Errors: External system interaction issues
   - API failures and rate limiting
   - Data format mismatches
   - Version compatibility issues
   - Authentication and authorization failures

ERROR HANDLING STANDARDS:
☐ Error categories are consistently applied across agents
☐ Error messages include sufficient context for resolution
☐ Error codes follow domain-wide numbering scheme
☐ Retry logic is appropriate for error type
☐ Error escalation paths are clearly defined
☐ Error recovery procedures are documented and tested
```

---

## **PATTERN 5: INTEGRATION VALIDATION FRAMEWORK**

### **Universal Integration Pattern**
```
For any Guardian Agent domain [X]:

INTEGRATION POINT MAPPING:
1. Upstream Integrations: What feeds data into this agent?
   - Other Guardian agents in workflow chains
   - External APIs and data sources
   - User inputs and configuration
   - Scheduled jobs and triggers

2. Downstream Integrations: What consumes this agent's output?
   - Subsequent agents in workflow chains
   - External systems and APIs
   - User interfaces and reports
   - Audit logs and compliance systems

3. Lateral Integrations: What peer-level interactions exist?
   - Shared data sources and caches
   - Common configuration systems
   - Monitoring and logging infrastructure
   - Authentication and authorization services

4. Emergency Integrations: What happens during failures?
   - Fallback data sources and services
   - Emergency notification systems
   - Manual override procedures
   - Recovery and restoration processes

INTEGRATION VALIDATION:
☐ All integration points are explicitly documented
☐ Integration contracts (APIs, data formats) are versioned
☐ Integration failures are handled gracefully
☐ Integration performance is monitored and alerted
☐ Integration changes follow proper change management
☐ Integration tests validate end-to-end scenarios
```

---

## **PATTERN 6: COMPLEXITY ASSESSMENT FRAMEWORK**

### **Universal Over-Engineering Detection**
```
For any Guardian Agent domain [X]:

COMPLEXITY INDICATORS:
1. Functional Complexity: Is the solution appropriate for the problem?
   - Lines of code vs business value delivered
   - Number of configuration options vs actual usage
   - API surface area vs required functionality
   - Performance optimization vs actual performance requirements

2. Technical Complexity: Is the technical approach justified?
   - Technology stack size vs problem complexity
   - Abstraction layers vs maintainability benefits
   - External dependencies vs functionality provided
   - Architecture patterns vs team capability

3. Operational Complexity: Is the operational overhead reasonable?
   - Deployment steps vs automation benefits
   - Monitoring configuration vs operational insights
   - Troubleshooting procedures vs failure frequency
   - Maintenance overhead vs business criticality

4. Cognitive Complexity: Is the mental model manageable?
   - Concepts to understand vs team expertise
   - Documentation required vs onboarding time
   - Testing complexity vs quality assurance needs
   - Change complexity vs feature velocity

SIMPLIFICATION OPPORTUNITIES:
☐ Identify features used by <20% of users (candidate for removal)
☐ Find abstractions with single implementations (remove abstraction)
☐ Locate configuration options never changed from defaults
☐ Discover performance optimizations that don't improve actual performance
☐ Remove dependencies that provide minimal value
☐ Simplify error handling for scenarios that never occur
```

---

## **PATTERN 7: BEST PRACTICES COMPLIANCE**

### **Universal Best Practices Framework**
```
For any Guardian Agent domain [X]:

DESIGN BEST PRACTICES:
☐ Single Responsibility: Agent has one clear, well-defined purpose
☐ Open/Closed Principle: Extensible behavior without modification
☐ Interface Segregation: Clean, minimal interfaces between agents
☐ Dependency Inversion: Depends on abstractions, not concretions
☐ Composition over Inheritance: Flexible component relationships

IMPLEMENTATION BEST PRACTICES:
☐ Consistent coding standards and style guidelines
☐ Comprehensive test coverage (unit, integration, end-to-end)
☐ Clear documentation and examples
☐ Proper error handling and logging
☐ Security considerations integrated throughout

OPERATIONAL BEST PRACTICES:
☐ Comprehensive monitoring and alerting
☐ Automated deployment and rollback procedures
☐ Performance testing and optimization
☐ Disaster recovery and business continuity
☐ Regular security audits and updates

COLLABORATION BEST PRACTICES:
☐ Clear ownership and responsibility model
☐ Regular review and feedback processes
☐ Knowledge sharing and documentation
☐ Onboarding materials for new team members
☐ Change management and communication procedures
```

---

## **PATTERN 8: COMPLETENESS AUDIT FRAMEWORK**

### **Universal Completeness Checklist**
```
For any Guardian Agent domain [X]:

FUNCTIONAL COMPLETENESS:
☐ All specified requirements are implemented
☐ Alternative user paths are supported
☐ Error scenarios are handled appropriately
☐ Edge cases and boundary conditions are addressed
☐ Performance requirements are met

INTEGRATION COMPLETENESS:
☐ All required integrations are implemented and tested
☐ Integration error handling is comprehensive
☐ Data flow between components is validated
☐ API contracts are stable and versioned
☐ End-to-end workflows are tested

OPERATIONAL COMPLETENESS:
☐ Deployment procedures are documented and automated
☐ Monitoring and alerting are comprehensive
☐ Backup and recovery procedures are tested
☐ Security requirements are implemented and verified
☐ Performance tuning is complete and documented

DOCUMENTATION COMPLETENESS:
☐ User documentation is complete and current
☐ Developer documentation includes examples
☐ API documentation is comprehensive and accurate
☐ Troubleshooting guides are available
☐ Change logs are maintained
```

---

## **PATTERN 9: CONSTITUTIONAL COMPLIANCE**

### **Universal Constitutional Adherence**
```
For any Guardian Agent domain [X]:

GUARDIAN AGENT PRINCIPLES:
☐ Agent specialization is unique and non-overlapping
☐ Model optimization (Haiku vs Sonnet) is appropriate for task complexity
☐ Automatic chaining triggers are clearly defined and tested
☐ Performance SLAs are documented and monitored
☐ Validation framework compliance is maintained

ARCHITECTURAL PRINCIPLES:
☐ Agents are independently deployable and maintainable
☐ Dependencies are minimized and explicitly declared
☐ Interface contracts are stable and versioned
☐ Configuration is externalized and environment-specific
☐ State management is consistent and predictable

QUALITY PRINCIPLES:
☐ Test-driven development practices are followed
☐ Code quality standards are maintained and enforced
☐ Security requirements are integrated throughout
☐ Performance requirements are met and monitored
☐ Documentation is complete and current

OPERATIONAL PRINCIPLES:
☐ Deployment is automated and repeatable
☐ Monitoring provides actionable insights
☐ Error handling provides meaningful user feedback
☐ Recovery procedures are documented and tested
☐ Change management follows established processes
```

---

## **PATTERN 10: GO/NO-GO DECISION FRAMEWORK**

### **Universal Decision Matrix**
```
For any Guardian Agent domain [X]:

DECISION CRITERIA SCORING (1-5 scale):

TECHNICAL READINESS:
□ Implementation Quality: Code meets standards and best practices
□ Test Coverage: Comprehensive testing at all levels
□ Performance: Meets or exceeds SLA requirements
□ Security: Passes security review and testing
□ Integration: All integrations tested and validated

OPERATIONAL READINESS:
□ Deployment: Automated and tested deployment procedures
□ Monitoring: Comprehensive monitoring and alerting
□ Documentation: Complete user and operator documentation
□ Support: Support procedures and escalation paths defined
□ Recovery: Disaster recovery and business continuity tested

BUSINESS READINESS:
□ Value: Clear business value and success metrics
□ Stakeholders: Stakeholder buy-in and commitment
□ Resources: Adequate resources for launch and operation
□ Timeline: Realistic timeline and milestone planning
□ Risk: Acceptable risk level and mitigation plans

DECISION LOGIC:
- Average score ≥4.0 across all categories = GO
- Any score <3.0 in critical areas = NO-GO
- Critical risks unmitigated = NO-GO
- Score 3.0-3.9 average = CONDITIONAL GO (with improvement plan)

OUTPUT RECOMMENDATION:
Decision: [GO/NO-GO/CONDITIONAL GO]
Critical Issues: [List blocking issues]
Risk Level: [Low/Medium/High/Critical]
Mitigation Plan: [Required actions before GO]
Timeline: [Estimated effort to address issues]
Confidence: [Success probability percentage]
```

This universal framework ensures every Guardian Agent undergoes the same rigorous validation while adapting to domain-specific requirements and constraints.
