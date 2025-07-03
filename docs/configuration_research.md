# Configuration Research

## VSCode MCP Server Configuration

**Official Documentation:** https://code.visualstudio.com/docs/copilot/chat/mcp-servers

- **User Settings:** Global MCP server configuration in user settings.json
  - **macOS:** `$HOME/Library/Application Support/Code/User/settings.json`
  - **Linux:** `$HOME/.config/Code/User/settings.json`
  - **Windows:** `%APPDATA%\Code\User\settings.json`
  - Configuration format: `{ "servers": { ... } }`
- **Workspace Settings:** Project-specific MCP server configuration
  - Located in `<project-root>/.vscode/mcp.json`
  - Configuration format: `{ "servers": { ... } }`

## Claude Desktop MCP Server Configuration

**Official Documentation:** https://modelcontextprotocol.io/quickstart/user

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- Configuration format: `{ "mcpServers": { ... } }`

## Gemini CLI MCP Server Configuration

**Official Documentation:** https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md

- **User Settings:** Global MCP server configuration
  - **Location:** `~/.gemini/settings.json`
  - **Scope:** Applies to all Gemini CLI sessions for the current user
- **Project Settings:** Project-specific MCP server configuration
  - **Location:** `<project-root>/.gemini/settings.json`
  - **Scope:** Applies only when running Gemini CLI from that specific project (overrides user settings)
- **Configuration format:** `{ "mcpServers": { ... } }`
