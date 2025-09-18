# Reference Materials

This directory contains all the original source materials that were used to create the unified MetaSpec-Kyocera system. These files are preserved for reference and to maintain the complete development history.

## 📁 Directory Structure

### original-sources/
Contains complete copies of all original repositories, excluding git metadata:

#### DeepResearchAgent/
- **Source**: `/home/kkk/Apps/deep-research/DeepResearchAgent-main/`
- **Description**: Hierarchical multi-agent framework for complex task solving and deep research
- **Key Components**:
  - `src/agent/` - Core agent system
  - `src/models/` - Multi-provider model support
  - `src/tools/` - Tool integrations
  - `configs/` - Configuration files
  - `docs/` - Comprehensive documentation

#### claude-guardian-agents/
- **Source**: `/home/kkk/Apps/deep-research/claude-guardian-agents-main/`
- **Description**: 52 specialized AI agents (49 + 3 meta-agents) for software development
- **Key Components**:
  - `1-product/` - Product management and design agents
  - `2-engineering/` - Technical and architecture agents
  - `3-operations/` - Operations and security agents
  - `4-thinktank/` - Think-tank reasoning agents
  - `5-meta-agents/` - Meta-orchestration agents

#### MonthlyKyocera/
- **Source**: `/home/kkk/Apps/deep-research/MonthlyKyocera-main/`
- **Description**: Kyocera meter reading management system (existing implementation)
- **Key Components**:
  - `scripts/` - Processing scripts
  - `devices/` - Device data organization
  - `emails/` - Email processing
  - `.claude/agents/` - Agent configurations
  - `.archive/` - Archived emails with short names

#### spec-kit/
- **Source**: `/home/kkk/Apps/spec-kit/`
- **Description**: Spec-driven development toolkit for building high-quality software
- **Key Components**:
  - `src/specify_cli/` - CLI tool for project initialization
  - `templates/` - Specification templates
  - `scripts/` - Build and setup scripts
  - `docs/` - Usage documentation

## 🔄 Relationship to MetaSpec-Kyocera

### How These Sources Were Integrated

1. **DeepResearchAgent** → **core/orchestration/**
   - Agent system migrated to unified orchestration
   - Model management integrated
   - Tool system enhanced

2. **claude-guardian-agents** → **core/agents/**
   - 52 agents integrated into unified system
   - Kyocera-specific agents added
   - Agent workflows enhanced

3. **spec-kit** → **specs/**
   - Workflow templates integrated
   - CLI tools adapted for Kyocera domain
   - Specification-driven development adopted

4. **MonthlyKyocera** → **domains/kyocera/**
   - Existing functionality preserved
   - Enhanced with unified architecture
   - Data and email archives maintained

### Preserved Elements

- **All source code** - Complete original implementations
- **Documentation** - All README files, guides, and specifications
- **Configuration files** - All config, YAML, JSON, and setup files
- **Data structures** - Email archives, device registries, test data
- **Asset files** - Images, media, templates, and resources

### Excluded Elements

- **Git metadata** - `.git/` directories not copied (prevents repository conflicts)
- **Cache files** - `__pycache__/`, `.mypy_cache/`, `node_modules/` excluded
- **Build artifacts** - `dist/`, `build/` directories not included
- **Environment files** - Local `.env` files excluded for security

## 📚 Using Reference Materials

### For Development
- Reference original implementations when enhancing unified system
- Use original documentation for context and design decisions
- Preserve original patterns and conventions where appropriate

### For Troubleshooting
- Compare unified implementation with original source
- Check original configurations for missing settings
- Reference original documentation for usage patterns

### For Enhancement
- Extract additional features from original repositories
- Adapt original agent configurations for new use cases
- Reference original test patterns for comprehensive testing

## 🔍 Finding Specific Information

### Email Processing
- **MonthlyKyocera/scripts/** - Original processing scripts
- **MonthlyKyocera/.archive/** - Email archival examples
- **MonthlyKyocera/devices/** - Device organization patterns

### Agent Configurations
- **claude-guardian-agents/[1-5]-*/** - All 52 agent definitions
- **MonthlyKyocera/.claude/agents/** - Kyocera-specific agents
- **DeepResearchAgent/src/agent/** - Core agent architecture

### Specifications and Workflows
- **spec-kit/templates/** - Specification templates
- **spec-kit/scripts/** - Build and workflow scripts
- **DeepResearchAgent/configs/** - Configuration patterns

### Documentation Patterns
- ***/docs/** directories in all sources
- ***/README.md** files throughout repositories
- **DeepResearchAgent/docs/** - Comprehensive documentation examples

## ⚠️ Important Notes

### Do Not Modify
These reference materials should **NOT** be modified. They serve as:
- Historical record of original implementations
- Reference for debugging and enhancement
- Backup of original functionality

### Development Guidelines
When working on the unified system:
1. **Reference** these materials for context
2. **Adapt** patterns to unified architecture
3. **Enhance** functionality in unified system
4. **Preserve** original design principles where appropriate

### File Integrity
- All files maintain original structure and content
- Symlinks preserved where they existed
- File permissions maintained from source
- Directory structure reflects original organization

---

**Last Updated**: 2025-09-19
**Source Repositories**: 4 (DeepResearchAgent, claude-guardian-agents, MonthlyKyocera, spec-kit)
**Total Files**: 1000+ preserved with complete functionality