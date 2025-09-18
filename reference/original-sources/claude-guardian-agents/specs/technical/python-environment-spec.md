# Python Environment Specification

## 🎯 Overview

This specification defines the Python environment management strategy for Guardian Agents project, using `uv` as the exclusive tool for all Python dependency management, virtual environment operations, and package installation.

## 📋 Requirements

### **Functional Requirements**
- **F1**: All Python operations must use `uv` exclusively
- **F2**: No direct `pip`, `pipenv`, `conda`, or `poetry` usage allowed
- **F3**: Virtual environment must be managed by `uv`
- **F4**: Development dependencies must be optional and clearly separated
- **F5**: Cross-platform compatibility (Linux, macOS, Windows)

### **Non-Functional Requirements**
- **NF1**: Environment setup time < 2 minutes
- **NF2**: Reproducible builds across all environments
- **NF3**: Dependency resolution must be deterministic
- **NF4**: Development tools must integrate seamlessly

## 🏗️ Technical Architecture

### **Project Structure**
```
guardian-agents/
├── pyproject.toml              # Project metadata and dependencies
├── .python-version             # Python version specification
├── .pre-commit-config.yaml     # Code quality automation
├── Makefile                    # Development workflow commands
├── activate-env.sh             # Environment activation helper
├── scripts/
│   ├── setup-python-env.sh    # Environment setup automation
│   ├── track-progress.py       # Progress tracking (Python)
│   └── generate-reports.py     # Report generation (Python)
└── .venv/                      # Virtual environment (uv-managed)
```

### **Dependency Management Strategy**

#### **Core Dependencies**
```toml
dependencies = [
    "pyyaml>=6.0",              # YAML processing
    "requests>=2.28.0",         # HTTP client
    "rich>=13.0.0",             # Terminal formatting
    "click>=8.0.0",             # CLI framework
    "python-dateutil>=2.8.0",  # Date/time utilities
]
```

#### **Development Dependencies**
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",           # Testing framework
    "pytest-cov>=4.0.0",       # Coverage reporting
    "black>=23.0.0",           # Code formatting
    "ruff>=0.1.0",             # Linting and import sorting
    "mypy>=1.0.0",             # Type checking
    "pre-commit>=3.0.0",       # Git hooks
]
```

## 🔧 Implementation Details

### **Environment Setup Process**

1. **Verification Phase**
   ```bash
   # Check uv installation
   uv --version || exit 1
   ```

2. **Environment Creation**
   ```bash
   # Remove existing environment
   rm -rf .venv

   # Create new environment with specific Python version
   uv venv .venv --python 3.11
   ```

3. **Dependency Installation**
   ```bash
   # Install project with all optional dependencies
   uv pip install -e ".[dev,docs,validation]"
   ```

4. **Tool Configuration**
   ```bash
   # Install pre-commit hooks
   pre-commit install

   # Make scripts executable
   chmod +x scripts/*.sh scripts/*.py
   ```

### **Development Workflow Integration**

#### **Makefile Targets**
```makefile
# Setup
install:     uv pip install -e .
dev-install: uv pip install -e ".[dev,docs,validation]"

# Quality Assurance
test:        pytest tests/ -v --cov=src
lint:        ruff check src/ scripts/ tests/
format:      black src/ scripts/ tests/
check:       lint test

# Project Management
reports:     python scripts/generate-reports.py all
validate:    python scripts/validate-gmp.py
track:       python scripts/track-progress.py calculate-completion
```

#### **Pre-commit Integration**
```yaml
repos:
  - repo: local
    hooks:
      - id: uv-check
        name: uv dependency check
        entry: uv pip check
```

## 🧪 Validation Framework

### **Environment Validation**
```bash
#!/bin/bash
# Validate uv-managed environment

# 1. Check uv installation
uv --version

# 2. Verify virtual environment
[ -d .venv ] && echo "✅ Virtual environment exists"

# 3. Test dependency installation
python -c "import yaml, requests, rich, click" && echo "✅ Core dependencies working"

# 4. Validate development tools
black --check scripts/ && echo "✅ Black formatting validated"
ruff check scripts/ && echo "✅ Ruff linting validated"
pytest --collect-only && echo "✅ Pytest configuration validated"
```

### **Cross-Platform Testing**
- **Linux**: Ubuntu 20.04+ with uv installed
- **macOS**: macOS 12+ with uv via Homebrew
- **Windows**: Windows 10+ with uv via PowerShell

## 📊 Quality Gates

### **Code Quality Standards**
- **Coverage**: Minimum 80% test coverage
- **Formatting**: Black with 88-character line length
- **Linting**: Ruff with strict rule set
- **Type Checking**: MyPy with strict mode
- **Security**: Bandit security scanning

### **Performance Requirements**
- **Setup Time**: < 2 minutes from clean state
- **Test Execution**: < 30 seconds for full test suite
- **Dependency Resolution**: < 10 seconds for uv operations

## 🔄 Automation Integration

### **CI/CD Pipeline**
```yaml
# Example GitHub Actions integration
steps:
  - uses: actions/checkout@v4
  - uses: astral-sh/setup-uv@v1
    with:
      version: "latest"
  - run: uv venv .venv --python 3.11
  - run: uv pip install -e ".[dev,docs,validation]"
  - run: make check
```

### **Development Scripts**
All Python scripts must include uv-specific shebang and requirements:

```python
#!/usr/bin/env python3
"""
Script description
Requires: uv-managed virtual environment
Usage: python script.py [args]
"""
```

## 📝 Migration Strategy

### **From pip/virtualenv**
```bash
# 1. Remove old environment
rm -rf venv/ .venv/

# 2. Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Run setup script
./scripts/setup-python-env.sh
```

### **From poetry/pipenv**
```bash
# 1. Extract dependencies to pyproject.toml
# (manual process - review existing files)

# 2. Remove old files
rm poetry.lock Pipfile Pipfile.lock

# 3. Setup new environment
./scripts/setup-python-env.sh
```

## 🚨 Error Handling

### **Common Issues and Solutions**

1. **uv not installed**
   ```bash
   # Solution: Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Python version mismatch**
   ```bash
   # Solution: Use correct Python version
   uv venv .venv --python 3.11
   ```

3. **Dependency conflicts**
   ```bash
   # Solution: Reset environment
   rm -rf .venv
   uv venv .venv --python 3.11
   uv pip install -e ".[dev,docs,validation]"
   ```

4. **Permission errors**
   ```bash
   # Solution: Fix script permissions
   chmod +x scripts/*.sh scripts/*.py
   ```

## 📈 Success Metrics

### **Technical Metrics**
- **Setup Success Rate**: > 95% across all platforms
- **Build Reproducibility**: 100% deterministic builds
- **Dependency Resolution Time**: < 10 seconds average
- **Test Suite Performance**: < 30 seconds execution

### **Developer Experience Metrics**
- **Onboarding Time**: < 5 minutes for new developers
- **Environment Consistency**: Zero environment-related bugs
- **Tool Integration**: Seamless IDE and editor support
- **Documentation Quality**: Self-service setup success > 90%

---

**Document Version**: 1.0
**Last Updated**: 2025-09-11
**Owner**: Technical Team
**Dependencies**: uv>=0.1.0, Python>=3.8
