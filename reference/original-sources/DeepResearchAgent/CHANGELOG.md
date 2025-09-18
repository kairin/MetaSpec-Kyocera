# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - TUI Foundation System (2025-09-16)
- Added interactive task input system (`src/tui/` module)
  - `src/tui/interactive_main.py` - New interactive entry point with task parameter support
  - `src/tui/interactive_main_with_input.py` - Full TUI experience with Rich prompts
  - `src/tui/task_collector.py` - Interactive task collection with validation and templates
- Added comprehensive task validation system
  - Length validation (10-2000 characters)
  - Content validation (not purely numeric, contains alphabetic characters)
  - User-friendly error messages and retry logic
- Added task template system with 10 predefined research templates
  - Research Latest Papers, Analyze Website, Compare Technologies, Market Analysis
  - Code Review, Technical Documentation, Competitive Analysis, Literature Review
  - Data Analysis, Custom Task options with placeholder customization
- Added Rich library dependency for beautiful terminal UI
- Added three usage modes for user flexibility:
  1. Command line: `python main.py --task "Custom task"`
  2. Interactive TUI: `python src/tui/interactive_main_with_input.py --interactive`
  3. Default demo: `python main.py` (backward compatible)

### Fixed - Critical User Experience Issues (2025-09-16)
- **CRITICAL**: Fixed hardcoded task limitation that prevented custom user input
  - Modified `main.py` to accept `--task` parameter
  - Added task parameter to main() function: `async def main(task: str = None)`
  - Maintains full backward compatibility with existing usage
- **CRITICAL**: Fixed MarkItDown integration errors with latest version
  - Replaced deprecated `MediaConverter` with `AudioConverter`
  - Fixed `_page_converters` → `_converters` attribute issue
  - System now starts without MarkItDown import errors

### Changed - Documentation Consolidation (2025-09-16)
- Consolidated redundant planning documents to reduce documentation proliferation
  - Removed `TUI_ANALYSIS_AND_STRATEGY.md`, `TUI_COMPREHENSIVE_PLANNING_SUMMARY.md`, `IMPLEMENTATION_SUMMARY.md`
  - Created unified `TUI_IMPLEMENTATION_GUIDE.md` preserving all valuable content
  - Updated `CURRENT_STATUS_AND_NEXT_ACTIONS.md` with live status tracking
  - Updated `PROJECT_ROADMAP.md` and `detailed_todo_checklist.md` with completion status
- Improved AGENTS.md conciseness by linking to detailed documentation instead of duplication

### Added - CLI-First Model System
- Added CLI tool detection system (`src/models/cli_detector.py`)
  - Detects Claude Code CLI and Gemini CLI availability
  - Provides installation instructions for missing CLI tools
  - Maps API model names to CLI equivalents
- Added CLI model factory (`src/models/cli_models.py`)
  - Factory pattern for creating CLI model instances
  - Support for ClaudeCodeModel, GeminiCLIModel, and CLIBridgeModel
  - Interactive CLI session management
- Added CLI-first configuration (`configs/config_cli_fallback.py`)
  - Prioritizes CLI tools over API calls when available
  - Uses local models as fallbacks when CLI tools unavailable

### Fixed - HuggingFace Integration
- **CRITICAL**: Fixed HuggingFace API key environment variable spelling
  - Corrected `HUGGINEFACE_API_KEY` → `HUGGINGFACE_API_KEY` in both `.env` and code
  - Ensures proper authentication with HuggingFace Inference API
- Fixed HuggingFace model timeout issues
  - Increased timeout from 120s to 300s for better stability
  - Added proper token limits (4096) and temperature settings (0.1)
  - Enhanced error handling for Gateway Timeout scenarios
- Fixed model registration KeyError exceptions
  - Implemented intelligent model aliasing system
  - Maps unavailable API models to local alternatives
  - Prevents crashes when models are not configured

### Changed - Model Management
- Restructured ModelManager initialization for CLI-first priority
  - Step 1: Detect and register CLI tools
  - Step 2: Validate API configurations
  - Step 3: Register local fallback models
  - Step 4: Create model aliases for missing models
- Enhanced model aliasing with comprehensive mappings:
  - `claude-3.7-sonnet-thinking` → `qwen2.5-32b-instruct`
  - `gemini-2.5-pro` → `qwen2.5-14b-instruct`
  - `gpt-4.1`, `o1`, `o3` → `qwen2.5-32b-instruct`

### Changed - Poetry to uv Migration (Breaking Changes)
- **BREAKING**: Migrated from Poetry to uv for all Python dependency management
- **BREAKING**: Upgraded default Python version from 3.11 to 3.13 (Ubuntu 25.04+ system Python)
- **BREAKING**: Changed build system from `poetry-core` to `hatchling`
- **BREAKING**: All installation and development commands now use uv exclusively

### Added - Poetry to uv Migration
- Added `uv.lock` for deterministic dependency resolution
- Added comprehensive validation script (`scripts/validate_migration.py`) for migration verification
- Added `migration_validation_report.json` for automated validation reporting
- Added new Makefile targets:
  - `make venv-system`: Create virtual environment with system Python
  - `make install-dev`: Install with development dependencies
  - `make install-locked`: Install from lock file only
  - `make lint-fix`: Auto-fix linting issues with ruff

### Fixed - Poetry to uv Migration
- Fixed circular import issues in `src/tools/` modules by updating import paths
- Fixed markitdown API compatibility issues:
  - Updated import path: `markitdown._base_converter` → `markitdown._markitdown`
  - Fixed class inheritance: `AudioConverter` → `MediaConverter`
  - Updated method signatures for new API structure
- Fixed Python 3.13 compatibility issues with dependency versions
- Fixed numpy version conflicts between browser-use and latest numpy
- Resolved build system configuration issues with file discovery

### Removed - Poetry to uv Migration
- Removed `poetry.lock`
- Removed Poetry configuration from `pyproject.toml`
- Removed all Poetry commands from Makefile
- Removed Poetry dependencies and references from documentation

### Updated - Poetry to uv Migration
- Updated `pyproject.toml`:
  - Migrated from Poetry format to PEP 621 standard
  - Changed dependency format from `[tool.poetry.dependencies]` to `[project] dependencies`
  - Updated build system configuration
  - Added proper package discovery configuration
- Updated `Makefile`:
  - All commands now use uv instead of Poetry
  - Python 3.13 set as default version
  - Comprehensive targets for development workflow
- Updated dependency versions to latest compatible versions:
  - 420+ packages resolved and updated
  - Fixed version constraints for Python 3.13 compatibility
  - Maintained backward compatibility where possible

### Migration Guide

#### For Existing Developers
1. **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Clean old environment**: `rm -rf .venv poetry.lock`
3. **Create new environment**: `make venv-system` or `make venv`
4. **Install dependencies**: `make install`
5. **Verify migration**: `uv run python scripts/validate_migration.py`

#### Key Command Changes
| Old (Poetry) | New (uv) |
|-------------|----------|
| `poetry install` | `uv sync --all-extras` |
| `poetry run python main.py` | `uv run python main.py` |
| `poetry add package` | `uv add package` |
| `poetry remove package` | `uv remove package` |
| `poetry shell` | `source .venv/bin/activate` |

#### New Requirements
- **Python 3.13+** (Ubuntu 25.04+ system Python recommended)
- **uv 0.8+** for dependency management
- No Poetry installation required

### Technical Details

#### Dependency Resolution
- Migrated 420+ packages from Poetry lock to uv lock
- Resolved version conflicts between major dependencies
- Maintained compatibility with existing functionality
- Updated to latest stable versions where possible

#### Build System
- Changed from `poetry-core` to `hatchling` build backend
- Updated package discovery and file inclusion patterns
- Maintained compatibility with existing development tools

#### Python Compatibility
- Upgraded from Python 3.11 to Python 3.13 as default
- All dependencies verified for Python 3.13 compatibility
- Fixed syntax warnings and deprecation issues
- Maintained support for async/await patterns

### Validation
- ✅ 16 validation checks pass
- ✅ All core imports functional
- ✅ Clean environment creation works
- ✅ Build system properly configured
- ⚠️ Legacy references remain in dependency error messages (acceptable)

### Performance Impact
- Faster dependency resolution with uv
- Improved virtual environment creation speed
- Better caching and parallel operations
- Reduced installation time for development setup

---

## Previous Versions

### [0.1.0] - 2025-XX-XX
- Initial release with Poetry-based dependency management
- Python 3.11 support
- Hierarchical multi-agent framework
- Browser automation capabilities
- Model Context Protocol integration