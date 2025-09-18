# Quickstart Guide: Guardian Agent Specialization System

**Date**: 2025-09-09
**Audience**: Development teams implementing Guardian Agent system
**Duration**: 30 minutes to complete initial setup and validation

## Overview

This guide walks you through implementing the Guardian Agent specialization system with model optimization, validation framework, and workflow chains. You'll create your first specialized agent, validate it, and test the chaining system.

## Prerequisites

- Claude Code environment set up and functioning
- Access to repository with existing Guardian agents
- Basic understanding of YAML frontmatter and Markdown

## Quick Start Scenarios

### Scenario 1: Developer Creates Specialized Agent (10 minutes)

**Objective**: Create a new Git workflow agent with proper specialization and model assignment.

**Steps**:

1. **Create agent configuration**
   ```bash
   # Navigate to repository root
   cd /home/kkk/Apps/claude-guardian-agents

   # Create new Git workflow agent directory (if needed)
   mkdir -p git-workflow-agents
   ```

2. **Use agent template**
   ```yaml
   ---
   name: 101-git-branch-guardian
   description: Branch creation with timestamp-based naming convention. MUST BE USED for creating new Git branches with temporal tracking.
   model: claude-3-5-haiku  # Simple task - Haiku optimized
   tools: [bash, read_file, write_file]
   complexity: simple
   department: Infrastructure
   role: Branch Management
   specialization: Git branch naming and creation automation
   ---

   You are a Git branch management specialist focused on creating branches with temporal naming conventions.

   ## Your Role
   - Agent ID: 101
   - Department: Infrastructure
   - Role: Branch Management
   - Specialization: Automated branch creation with timestamp tracking

   ## Core Responsibilities
   - Generate branch names using YYYYMMDD-HHMM format
   - Validate branch naming conventions
   - Create branches with proper Git commands
   - Set up branch tracking and initial commit

   ## Agent Chaining Instructions
   After creating a branch, automatically delegate to:

   ### Sequential Chain:
   1. **102-git-naming-guardian** - For name validation
   2. **103-git-commit-guardian** - For initial commit setup

   ### Conditional Chains:
   - If feature branch → **106-git-feature-guardian**
   - If hotfix branch → **107-git-hotfix-guardian**
   - If experiment branch → **108-git-experiment-guardian**

   ## Trigger Phrases
   - "Create new branch for [task]"
   - "Need a branch for [feature]"
   - "Set up branch for [work]"
   ```

3. **Save agent file**
   ```bash
   # Create the agent file
   cat > git-workflow-agents/101-git-branch-guardian.md << 'EOF'
   [content from step 2]
   EOF
   ```

4. **Test agent invocation**
   ```bash
   # Test in Claude Code environment
   # Use the /task command to invoke the agent
   ```

**Expected Result**: Agent creates properly named branch with timestamp format like `feature/20250109-1430-user-authentication`

### Scenario 2: System Optimizes Model Selection (5 minutes)

**Objective**: Verify that the system automatically assigns appropriate models based on task complexity.

**Steps**:

1. **Test simple task routing (Haiku)**
   - Task: "Format commit message for bug fix"
   - Expected: Routes to Haiku-optimized agent (fast response <2s)

2. **Test complex task routing (Sonnet)**
   - Task: "Analyze security implications of new authentication system"
   - Expected: Routes to Sonnet-optimized agent (quality analysis)

3. **Monitor performance metrics**
   ```bash
   # Check response times and model assignments
   # Simple tasks: <2s with Haiku
   # Complex tasks: <10s with Sonnet
   ```

**Expected Result**: System demonstrates 70%+ cost reduction while maintaining quality standards

### Scenario 3: Validation Framework Verifies Agent Quality (10 minutes)

**Objective**: Run the validation framework against a Guardian Agent and interpret results.

**Steps**:

1. **Run agent validation**
   ```bash
   # Validate the newly created agent
   guardians validate --agent 101-git-branch-guardian
   ```

2. **Review validation output**
   ```
   Agent Validation Report: 101-git-branch-guardian
   Generated: 20250109-1530
   =============================================

   AGENT FOUNDATION: 7/8 ✓ (87.5%)
   ✓ Agent YAML configuration validates against schema
   ✓ Required tools are accessible and functional
   ✓ Model optimization (Haiku) configured correctly
   ✓ Agent chaining triggers work with next agents
   ✓ Error handling includes proper rollback capabilities
   ✓ Performance meets SLA requirements (<2s for Haiku)
   ☐ Agent not yet registered in central registry
   ✓ Agent works in Claude Code environment

   SPECIALIZATION: 6/6 ✓ (100%)
   ✓ Core responsibilities implemented and testable
   ✓ Input processing handles expected data formats
   ✓ Output format matches downstream agent requirements
   ✓ Trigger phrases activate automatic agent selection
   ✓ Conditional routing logic handles edge cases correctly
   ✓ Agent expertise area clearly differentiated from others

   INTEGRATION: 4/6 ✓ (66.7%)
   ✓ Upstream agent handoffs work seamlessly
   ✓ Downstream agent chains trigger appropriately
   ~ Multi-agent workflows partially complete (3/5 scenarios pass)
   ✓ Error recovery between agents functions properly
   ☐ Performance testing not yet complete
   ☐ Resource usage monitoring not configured

   OVERALL READINESS: 85% Complete
   - Critical blockers: 0
   - Minor issues: 3
   - Enhancement opportunities: 2

   Recommendations:
   1. Register agent in central registry (5 minutes)
   2. Complete performance testing suite (30 minutes)
   3. Configure resource monitoring (15 minutes)
   ```

3. **Address validation issues**
   - Fix identified blockers
   - Re-run validation to confirm improvements

**Expected Result**: Agent achieves 85%+ validation score with clear improvement path

### Scenario 4: Test Multi-Agent Workflow Chain (5 minutes)

**Objective**: Verify that agents properly chain together for complex workflows.

**Steps**:

1. **Initiate workflow chain**
   ```bash
   # Start a feature development workflow
   "Create and implement user authentication feature"
   ```

2. **Observe chaining sequence**
   ```
   Expected Chain:
   001-strategy-product-leadership-guardian (Sonnet)
   → 002-strategy-product-strategy-guardian (Sonnet)
   → 021-design-product-leadership-guardian (Sonnet)
   → 041-architecture-cto-leadership-guardian (Sonnet)
   → 061-development-backend-director-guardian (Sonnet)
   → 063-development-backend-junior-guardian (Haiku)
   → 101-git-branch-guardian (Haiku)
   ```

3. **Monitor performance**
   - Total workflow time: <2 minutes
   - Model switching: Sonnet for decisions, Haiku for execution
   - Context preservation across handoffs

**Expected Result**: End-to-end workflow completes successfully with proper agent specialization and handoffs

## Verification Checklist

### ✅ Agent Creation Success
- [ ] Agent file follows naming convention
- [ ] YAML frontmatter validates against schema
- [ ] Model assignment matches task complexity
- [ ] Specialization is clearly defined and unique
- [ ] Trigger phrases enable automatic selection

### ✅ Model Optimization Working
- [ ] Simple tasks route to Haiku agents (<2s response)
- [ ] Complex tasks route to Sonnet agents (<10s response)
- [ ] Cost reduction visible (target: 70-85%)
- [ ] Quality maintained (95%+ for most tasks)

### ✅ Validation Framework Functional
- [ ] Validation runs without errors
- [ ] Multi-perspective checking works (dev/test/review/production)
- [ ] Status symbols display correctly (✓/☐/~/✗/⚠️)
- [ ] Remediation guidance provided for issues
- [ ] Performance SLA monitoring active

### ✅ Workflow Chaining Operational
- [ ] Agent-to-agent handoffs preserve context
- [ ] Conditional routing works based on task type
- [ ] Error recovery triggers appropriate agents
- [ ] End-to-end workflows complete successfully

## Troubleshooting Common Issues

### Issue: Agent Not Auto-Selected
**Symptoms**: Manual agent specification required, automatic selection fails
**Solution**:
1. Check description contains "MUST BE USED" phrase
2. Verify trigger patterns are unique and specific
3. Ensure agent is registered in central registry

### Issue: Model Assignment Incorrect
**Symptoms**: Haiku used for complex tasks, or Sonnet for simple tasks
**Solution**:
1. Verify complexity field matches task type
2. Check model assignment aligns with complexity
3. Update routing rules if needed

### Issue: Validation Framework Errors
**Symptoms**: Validation fails with schema errors
**Solution**:
1. Validate YAML syntax and structure
2. Check required fields are present
3. Verify tool names are valid Claude Code tools

### Issue: Poor Chain Performance
**Symptoms**: Workflows take too long or fail frequently
**Solution**:
1. Check individual agent SLA compliance
2. Verify context preservation between agents
3. Review error handling and recovery mechanisms

## Next Steps

After completing the quickstart:

1. **Scale Up**: Create additional specialized agents for your specific domain
2. **Optimize**: Monitor performance metrics and adjust model assignments
3. **Integrate**: Connect with existing development workflows and tools
4. **Validate**: Run comprehensive validation on all agents
5. **Document**: Update agent documentation and workflow diagrams

## Support and Resources

- **Agent Templates**: `/templates/agent-file-template.md`
- **Validation Guide**: `/templates/validation-template.md`
- **Model Optimization**: `/templates/model-optimization-guide.md`
- **Workflow Examples**: `/docs/workflows/`
- **Performance Monitoring**: `/docs/monitoring/`

**Estimated Total Time**: 30 minutes
**Complexity**: Beginner to Intermediate
**Success Rate**: 95% with proper setup

This quickstart provides hands-on experience with the core Guardian Agent system capabilities, demonstrating specialization, model optimization, validation, and workflow chaining in practical scenarios.
