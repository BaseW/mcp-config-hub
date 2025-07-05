#!/usr/bin/env bash
# Quality check script using uv
set -e
uv pip install .[dev]

# Lint
uv run ruff check src/ tests/

# Type check
uv run mypy src/ tests/

# Format check
uv run black --check src/ tests/
uv run isort --check src/ tests/

# Security check
uv run bandit -r src/

# Dependency vulnerability check
uv run pip-audit
