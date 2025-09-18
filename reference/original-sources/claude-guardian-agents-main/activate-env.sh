#!/bin/bash
# Guardian Agents Environment Activation Helper
# Ensures uv virtual environment is properly activated

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "❌ Virtual environment not found. Run: ./scripts/setup-python-env.sh"
    exit 1
fi

source "$PROJECT_ROOT/.venv/bin/activate"
echo "✅ Guardian Agents environment activated (using uv)"
echo "Python: $(python --version)"
echo "Location: $(which python)"
