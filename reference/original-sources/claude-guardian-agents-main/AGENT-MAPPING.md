# Agent Mapping - Existing Structure to New Naming Convention

## Current Directory Structure Preserved

Your existing organizational structure will be maintained:
- `1-product/` - Product management and design teams
- `2-engineering/` - Technical development teams  
- `3-operations/` - Operations and support teams

## Mapping Strategy

Instead of moving files, I'll **rename them in-place** using this mapping:

### 1-product/ Directory

#### 1-product-management/
- `cpo-guardian.md` → `001-strategy-product-leadership-guardian.md`

##### 1-product-strategy/
- `pds-guardian.md` → `002-strategy-product-strategy-guardian.md`
- `psm-guardian.md` → `003-strategy-product-management-guardian.md`

##### 2-product-ownership/
- `ppo-guardian.md` → `004-strategy-product-ownership-guardian.md`
- `spo-guardian.md` → `005-strategy-product-senior-guardian.md`
- `apo-guardian.md` → `006-strategy-product-associate-guardian.md`

#### 2-product-design/
- `cpd-guardian.md` → `021-design-product-leadership-guardian.md`

##### 1-ux-research/
- `uxr-guardian.md` → `022-design-ux-research-guardian.md`
- `jur-guardian.md` → `023-design-ux-junior-guardian.md`

##### 2-ui-design/
- `uid-guardian.md` → `024-design-ui-interface-guardian.md`
- `jui-guardian.md` → `025-design-ui-junior-guardian.md`

### 2-engineering/ Directory

#### 1-cto-office/
- `cto-guardian.md` → `041-architecture-cto-leadership-guardian.md`
- `tfe-guardian.md` → `042-architecture-technical-fellow-guardian.md`

#### 2-software-engineering/
- `vps-guardian.md` → `043-architecture-vp-engineering-guardian.md`

##### 1-architecture/
- `par-guardian.md` → `044-architecture-principal-architect-guardian.md`
- `sar-guardian.md` → `045-architecture-senior-architect-guardian.md`

##### 2-backend-engineering/
- `dbe-guardian.md` → `061-development-backend-director-guardian.md`
- `sbe-guardian.md` → `062-development-backend-senior-guardian.md`
- `jbe-guardian.md` → `063-development-backend-junior-guardian.md`

##### 3-frontend-engineering/
- `dfe-guardian.md` → `064-development-frontend-director-guardian.md`
- `sfe-guardian.md` → `065-development-frontend-senior-guardian.md`
- `jfe-guardian.md` → `066-development-frontend-junior-guardian.md`

##### 4-mobile-engineering/
- `dme-guardian.md` → `067-development-mobile-director-guardian.md`
- `sme-guardian.md` → `068-development-mobile-senior-guardian.md`
- `jme-guardian.md` → `069-development-mobile-junior-guardian.md`

#### 3-quality-engineering/
- `dqe-guardian.md` → `071-development-quality-director-guardian.md`
- `sqe-guardian.md` → `072-development-quality-senior-guardian.md`
- `jqe-guardian.md` → `073-development-quality-junior-guardian.md`

#### 4-devops-engineering/
- `dde-guardian.md` → `081-infrastructure-devops-director-guardian.md`
- `sde-guardian.md` → `082-infrastructure-devops-senior-guardian.md`
- `jde-guardian.md` → `083-infrastructure-devops-junior-guardian.md`

### 3-operations/ Directory

#### 1-coo-office/
- `coo-guardian.md` → `091-operations-coo-leadership-guardian.md`

#### 2-security-operations/
- `dso-guardian.md` → `092-security-operations-director-guardian.md`
- `sse-guardian.md` → `093-security-operations-senior-guardian.md`
- `jse-guardian.md` → `094-security-operations-junior-guardian.md`

#### 3-data-operations/
- `ddo-guardian.md` → `095-data-operations-director-guardian.md`
- `sde-guardian.md` → `096-data-operations-senior-guardian.md`
- `jde-guardian.md` → `097-data-operations-junior-guardian.md`

#### 4-it-operations/
- `dio-guardian.md` → `098-operations-it-director-guardian.md`
- `sit-guardian.md` → `099-operations-it-senior-guardian.md`
- `jit-guardian.md` → `100-operations-it-junior-guardian.md`

## Numbering System Logic

- **001-020**: Strategic Leadership & Product Strategy
- **021-040**: Design & User Experience  
- **041-060**: Technical Architecture & Leadership
- **061-080**: Development Teams (Backend, Frontend, Mobile)
- **081-090**: Infrastructure & DevOps
- **091-100**: Operations & Security

## Benefits of This Approach

1. **Preserves Your Structure**: Existing folders remain intact
2. **Maintains Hierarchy**: Organizational reporting structure preserved
3. **Adds Process Order**: Numbers indicate workflow sequence
4. **Easy Migration**: Simple file renames, no directory restructuring
5. **Backwards Compatible**: Links and references can be updated incrementally

## Implementation Plan

1. Rename files in-place using git mv
2. Update internal file content with new naming
3. Update AGENTS.md hierarchy diagram
4. Update all cross-references
5. Test agent invocations work correctly

---

**This mapping respects your existing organizational structure while implementing the process-flow numbering system.**