# Configuration Research

## VSCode MCP Server Configuration

**Official Documentation:** https://code.visualstudio.com/docs/copilot/chat/mcp-servers

- **User Settings:** Global MCP server configuration in user settings.json
  - **macOS:** `$HOME/Library/Application Support/Code/User/settings.json`
  - **Linux:** `$HOME/.config/Code/User/settings.json`
  - **Windows:** `%APPDATA%\Code\User\settings.json`
  - Configuration format: `"mcp": { "servers": { ... } }`
- **Workspace Settings:** Project-specific MCP server configuration
  - Located in `<project-root>/.vscode/mcp.json`

## Claude Desktop MCP Server Configuration

**Official Documentation:** https://modelcontextprotocol.io/quickstart/user

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

## ChatGPT MCP Server Configuration

**Status:** No official MCP server configuration documentation found for ChatGPT as of current research. This integration may be experimental or not yet officially supported.

## Gemini CLI

- The configuration file is typically located at `~/.gemini/settings.json`.
- Project-specific configurations can be created by placing a `.gemini/settings.json` file in the project's root directory.
- **Note:** No official MCP server configuration documentation found for Gemini CLI.
