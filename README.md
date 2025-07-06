# MCP Config Hub

CLI tool for managing MCP server settings.

## Installation

```bash
pip install -e .
```

## Usage

### Basic Commands

```bash
# List all configurations
mcp-config list

# Get a specific configuration value
mcp-config get mcpServers.filesystem.command

# Set a configuration value
mcp-config set mcpServers.filesystem.command "npx"
mcp-config set mcpServers.filesystem.args '["@modelcontextprotocol/server-filesystem", "/path/to/directory"]

# Set a default prompt
mcp-config set-prompt "You are a helpful AI assistant." --scope user

# Different output formats
mcp-config list --format yaml
mcp-config list --format toml

# Different scopes
mcp-config list --scope user
mcp-config list --scope global
mcp-config list --scope project
```

### Configuration Scopes

- **Global**: System-wide configuration (`/etc/mcp-config-hub/config.json` on Linux/macOS)
- **User**: User-specific configuration (`~/.config/mcp-config-hub/config.json` on Linux)
- **Project**: Project-specific configuration (`.mcp-config-hub/config.json` in current directory)
- **Merged**: Combined configuration with project > user > global precedence

### Tool Integration

```bash
# Sync with VSCode
mcp-config sync vscode --direction from-hub
mcp-config sync vscode --direction to-hub

# Sync with Claude Desktop
mcp-config sync claude --direction from-hub
mcp-config sync claude --direction to-hub

# Sync with Cursor
mcp-config sync cursor --direction from-hub
mcp-config sync cursor --direction to-hub

# Sync with Windsurf
mcp-config sync windsurf --direction from-hub
mcp-config sync windsurf --direction to-hub

# Sync with Gemini CLI
mcp-config sync gemini --direction from-hub
mcp-config sync gemini --direction to-hub
```

## Supported Applications for Default Prompt

- **VSCode (GitHub Copilot)**: Manages `.github/copilot-instructions.md`
- **Cursor**: Manages `.cursor/rules/default_prompt.txt` (project-specific)
- **Windsurf**: Manages `.windsurfrules` (project-specific)
- **Gemini CLI**: Manages `GEMINI.md` (project-specific)
- **Claude Desktop**: Direct prompt setting not supported; context provided via MCP server.

## Configuration Format

The tool uses the standard MCP configuration format:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"]
    },
    "database": {
      "command": "python",
      "args": ["-m", "mcp_server_database", "--connection-string", "sqlite:///data.db"]
    }
  }
}
```

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Run the CLI directly
python main.py --help
```