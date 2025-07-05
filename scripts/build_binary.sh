# PyInstaller build script for mcp-config-hub
# Usage: bash scripts/build_binary.sh

set -e

# Clean previous build
rm -rf dist build *.spec

# Build binary with PyInstaller
/Users/yugo/ghq/github.com/BaseW/mcp-config-hub/.venv/bin/pyinstaller --onefile src/mcp_config_hub/cli.py --name mcp-config-hub

echo "Build complete. Binary is in dist/mcp-config-hub"
