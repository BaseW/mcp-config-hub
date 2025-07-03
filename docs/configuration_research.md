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

## ChatGPT MCP Server Configuration

**Status:** No official MCP server configuration documentation found for ChatGPT as of current research. This integration may be experimental or not yet officially supported.

**Experimental Configuration Paths:**
- **macOS:** `~/Library/Application Support/ChatGPT/config.json`
- **Linux:** `~/.config/ChatGPT/config.json`
- **Windows:** `%APPDATA%\ChatGPT\config.json`
- **Experimental format:** `{ "mcpServers": { ... } }`

## Gemini CLI

**Status:** No official MCP server configuration documentation found for Gemini CLI.

**General Configuration Paths:**
- The configuration file is typically located at `~/.gemini/settings.json`.
- Project-specific configurations can be created by placing a `.gemini/settings.json` file in the project's root directory.
- **Note:** MCP server configuration format unknown for this tool.
