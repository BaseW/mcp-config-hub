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

## Cursor MCP Server Configuration

**Official Documentation:** https://docs.cursor.com/context/mcp

- **Global:** `~/.cursor/mcp.json` (macOS/Linux), `%USERPROFILE%\.cursor\mcp.json` (Windows)
- **Project:** `.cursor/mcp.json` in the project root
- **Configuration format:**

```json
{
  "mcpServers": {
    "sample-server": {
      "command": "npx",
      "args": ["-y", "mcp-server"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Windsurf MCP Server Configuration

**Official Documentation:** https://docs.windsurf.com/windsurf/cascade/mcp

- **Location:** `~/.codeium/windsurf/mcp_config.json`
- **Configuration format:**

```json
{
  "mcpServers": {
    "spinach": {
      "command": "npx",
      "args": ["-y", "@spinach.ai/spinach-mcp-stdio-server@latest"],
      "env": { "API_KEY": "<YOUR API KEY FROM SPINACH>" }
    }
  }
}
```
- Each server is listed under `mcpServers`. `command`/`args` for local, `serverUrl` for remote servers.

## Claude Code CLI MCP Server Configuration

- **User Settings:** `~/.claude/settings.json` (applies to all projects)
- **Project Settings:**
    - `.claude/settings.json` (project-specific, version controlled)
    - `.claude/settings.local.json` (personal project preferences, not version controlled)
- **Global MCP Server Configuration:** Within the `mcpServers` property of `~/.claude.json`.
- **Key MCP-Related Settings in `settings.json`:**
    - `MCP_TIMEOUT`: Timeout for MCP server to start.
    - `MCP_TOOL_TIMEOUT`: Timeout for MCP tool execution.
    - `MAX_MCP_OUTPUT_TOKENS`: Max tokens in responses from MCP tools.

### Claude Code CLI Prompt Configuration

- **`CLAUDE.md`**: Project-specific prompt setting. Create a `CLAUDE.md` file in the project root. Claude Code CLI will automatically load its content as additional context.
- **`/init` command**: Use `/init` within Claude Code CLI to generate an initial `CLAUDE.md` file.
- **`--system-prompt` flag**: Only for single-command executions, not for interactive sessions.

## Default Prompt Configuration

### VSCode (GitHub Copilot)

- **Instructions File:** Create a file named `copilot-instructions.md` inside the `.github` directory at the root of your project. Copilot will automatically use the content of this file as instructions.
- **Settings JSON:** You can also add instructions to your `settings.json` file (user or workspace) under the key `github.copilot.chat.instructions`.

### Claude Desktop App

- The Claude Desktop app does not have a direct feature to set a persistent custom system prompt.
- The primary method to provide context is through the **Model Context Protocol (MCP)**. You can configure an MCP server in `claude_desktop_config.json` to provide contextual information, which can include instructions for the AI.

### Cursor

- **Rules for AI:** Default prompts can be set in `Cursor > Settings > Cursor Settings` under "Rules for AI".
- **Project-specific Rules:** For project-specific prompts, you can create a `.cursor/rules` directory in your project's root.

### Windsurf

- **Global AI Rules:** Global prompts can be configured in the Windsurf settings panel.
- **Workspace AI Rules:** Project-specific prompts can be set by creating a `.windsurfrules` file in the project's root directory.

### Gemini CLI

- **Project-specific Prompt:** Create a `GEMINI.md` file in the root of your project. The contents of this file will be used as the default prompt for that project.
- **Global Prompt:** A global default prompt can be set using the `prompt` key in the `~/.gemini/settings.json` file, though this is less documented.
