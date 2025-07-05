#!/usr/bin/env bash
# Run tests using uv (assumed to be installed)
uv pip install .[dev]
uv run pytest --maxfail=1 --disable-warnings -q
