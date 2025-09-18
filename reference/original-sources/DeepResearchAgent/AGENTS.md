# AGENTS.md

> 🔧 **Migration Notice**: This fork uses uv exclusively and Python 3.13. All commands below use uv instead of Poetry. See [CHANGELOG.md](CHANGELOG.md) for migration details.

## Project Overview

DeepResearchAgent is a hierarchical multi-agent framework for complex task solving and deep research. A central planning agent coordinates specialized execution agents using an async, tool-based architecture with multi-provider model support.

**Quick Links:** [Architecture](docs/architecture/OVERVIEW.md) • [Quick Start](docs/usage/QUICK_START.md) • [Setup](docs/setup/ENVIRONMENT_SETUP.md) • [Models](docs/models/CONFIGURATION.md)

## Quick Setup

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and setup
uv sync --all-extras
uv run playwright install chromium --with-deps
cp .env.template .env

# Run examples
uv run python main.py --tui    # Interactive TUI launcher
uv run python main.py          # Default agent run
```

**Detailed Setup:** [docs/setup/ENVIRONMENT_SETUP.md](docs/setup/ENVIRONMENT_SETUP.md)

## Essential Commands

### Running
```bash
uv run python main.py --tui                              # TUI launcher (interactive menu)
uv run python main.py --config configs/config_cli_fallback.py  # CLI-first (recommended)
uv run python main.py                                          # Full hierarchical system
uv run python examples/run_general.py                          # Single agent
```

### Using on External Projects (Recommended)
```bash
# Keep DeepResearchAgent separate and use on any project
cd /path/to/DeepResearchAgent

# Create project-specific config
cp configs/config_cli_fallback.py configs/config_my_project.py

# Analyze external projects
uv run python main.py --config configs/config_my_project.py \
    --task "Analyze codebase in /path/to/external_project"

# Example: MonthlyKyocera analysis
uv run python main.py --task "Research Kyocera device performance patterns in /home/kkk/Apps/MonthlyKyocera"
```

### Testing
```bash
uv run pytest tests/unit/                               # Run unit tests only
uv run pytest tests/integration/                       # Run integration tests only
uv run python scripts/run_comprehensive_tests.py       # Comprehensive test runner (recommended)

# Test outputs are saved to test_output/ with unique timestamps:
# - test_run_YYYYMMDD_HHMMSS_microseconds_PID.log (detailed logs)
# - test_results_YYYYMMDD_HHMMSS_microseconds_PID.json (results)
# - test_results.json (latest results, backwards compatible)
```

### Development
```bash
uv add package-name                      # Add dependency
uv sync --all-extras                     # Install dependencies
uv run black . && uv run isort .         # Format code
uv run ruff check .                      # Lint code

# Development tools
uv run python tools/development/test_minimal_tui.py     # Test TUI functionality
uv run python tools/development/debug_terminal.py      # Debug terminal issues
```

**Complete Command Reference:** [docs/usage/COMMANDS.md](docs/usage/COMMANDS.md) • [File Organization](docs/FILE_ORGANIZATION.md)

## Configuration
```bash
# CLI-first (recommended for max subscriptions)
claude                                    # Local Claude Code CLI
gcloud cloud-shell ssh && gemini         # Google Cloud Shell Gemini
uv run python main.py --config configs/config_cli_fallback.py

# Local-only setup (offline development)
uv run python main.py --config configs/config_local_only.py
# Requires HUGGINGFACE_API_KEY in .env for model access

# Override settings
uv run python main.py --cfg-options agent_config.max_steps=10

# Environment setup
cp .env.template .env
# Configure as needed: HUGGINGFACE_API_KEY, optional: OPENAI_API_KEY, ANTHROPIC_API_KEY
```

**Full Guide:** [docs/models/CONFIGURATION.md](docs/models/CONFIGURATION.md)

## Development

### Architecture & Testing
- **Modular**: Agents in `src/agent/`, tools in `src/tools/`
- **Async**: All operations use asyncio
- **Config-driven**: MMEngine configuration system
- **Performance**: 83.39% GAIA benchmark average

#### Test Structure & Commands
```bash
# Test Commands
uv run pytest tests/unit/                    # Run unit tests only
uv run pytest tests/integration/            # Run integration tests only
uv run python scripts/run_comprehensive_tests.py --unit-only        # Comprehensive unit tests
uv run python scripts/run_comprehensive_tests.py --integration-only # Comprehensive integration tests
uv run python scripts/run_comprehensive_tests.py                    # Full test suite

# Test Output Locations
test_output/test_run_YYYYMMDD_HHMMSS_microseconds_PID.log    # Detailed logs (unique timestamps)
test_output/test_results_YYYYMMDD_HHMMSS_microseconds_PID.json # Test results (unique timestamps)
test_output/test_results.json                                 # Latest test results (backwards compatible)
```

**Test Organization:**
- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for end-to-end functionality
- `scripts/run_comprehensive_tests.py` - Comprehensive test runner with logging
- `test_output/` - All test logs and results with unique timestamps for historical tracking

**When running tests:** Always check `test_output/` for detailed logs and results. Each test run creates uniquely timestamped files to preserve historical data.

**Guidelines:** [docs/development/CONTRIBUTING.md](docs/development/CONTRIBUTING.md)

### 🚨 Git Archive Strategy

**EVERY COMMIT** must use archive branches:

```bash
DATETIME=$(date +"%Y%m%d-%H%M%S")
git checkout -b "archive/${DATETIME}-description"
git add . && git commit -m "Message"
git push -u origin "archive/${DATETIME}-description"
git checkout main && git merge "archive/${DATETIME}-description" --no-ff
```

**Full Git Guidelines:** [docs/development/GIT_STRATEGY.md](docs/development/GIT_STRATEGY.md)

### 🤖 LLM Conversation Logging

**MANDATORY REQUIREMENT**: All AI assistants (LLMs, Copilot, Claude, Gemini, etc.) working on this repository **MUST** save their complete conversation logs for the entire chat session.

#### Requirements:
- **Complete Logs**: Save the entire conversation from start to finish
- **Exclude Sensitive Data**: Remove all personal information, passwords, API keys, tokens, or similar sensitive data before saving
- **Storage Location**: Save logs in `docs/development/conversation_logs/` subdirectory
- **Naming Convention**: Use format `CONVERSATION_LOG_YYYYMMDD_DESCRIPTION.md`
- **Purpose**: Enable other developers to identify where errors occurred during LLM conversations and understand the full context of changes

#### Example:
```bash
# After completing work, save the conversation log:
cp /path/to/conversation_log.md docs/development/conversation_logs/CONVERSATION_LOG_20250917_test_improvements.md
```

**Why this matters**: LLM conversations often involve complex debugging, multiple iterations, and context that isn't captured in commit messages. These logs help future developers understand the reasoning behind changes and identify potential issues.

## Models
Connected models are validated at startup. Typical configuration includes:
- **CLI Tools**: Claude Code (`claude` command), Gemini (via `gcloud cloud-shell ssh`)
- **Local Models**: Qwen 2.5 series (7B/14B/32B) via HuggingFace API
- **Routing**: Primary CLI access with local model fallbacks

**Configuration:** [docs/models/CONFIGURATION.md](docs/models/CONFIGURATION.md)

## Security & MCP
- **Sandboxed execution**: Python restrictions, isolated browsers, API monitoring
- **MCP integration**: Dynamic tool discovery, local/remote tools, evolution

**Details:** [docs/security/GUIDELINES.md](docs/security/GUIDELINES.md)

## Troubleshooting

### 🚨 Emergency: Terminal Flooded with Mouse Escapes
If terminal shows continuous `<35;83;16M` sequences and you can't type:
```bash
# 1. Close terminal window → open new terminal (fastest)
# 2. Try rapid Ctrl+C if you can type
# 3. Quick fix: ./fix
```
**Emergency Guide:** [docs/TERMINAL_RECOVERY.md](docs/TERMINAL_RECOVERY.md)

### Standard Issues
```bash
uv sync --reinstall                     # Fix dependencies
uv run playwright install --force       # Fix browser automation

# Model validation (shows actual connected models)
uv run python -c "from src.models.model_validator import validate_and_display_models; validate_and_display_models()"

# API validation
uv run python -c "from src.models.api_validator import APIConfigValidator; APIConfigValidator().validate_all_configs()"

# TUI issues - use CLI mode instead:
uv run python main.py --config configs/config_cli_fallback.py

# Emergency mouse tracking fix:
uv run python tools/emergency/fix_mouse.py

# TUI testing:
uv run python tools/development/test_minimal_tui.py
```

**Full Guide:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## Documentation
[Setup](docs/setup/) • [Usage](docs/usage/) • [Architecture](docs/architecture/) • [Models](docs/models/) • [Development](docs/development/) • [Security](docs/security/)

**Index:** [docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)