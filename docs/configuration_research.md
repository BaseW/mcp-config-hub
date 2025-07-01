# Configuration Research

## VSCode

- **User Settings:** Global settings for all projects.
  - **macOS:** `$HOME/Library/Application Support/Code/User/settings.json`
  - **Linux:** `$HOME/.config/Code/User/settings.json`
  - **Windows:** `%APPDATA%\Code\User\settings.json`
- **Workspace Settings:** Project-specific settings that override user settings.
  - Located in `<project-root>/.vscode/settings.json`

## Gemini CLI

- The configuration file is typically located at `~/.gemini/settings.json`.
- Project-specific configurations can be created by placing a `.gemini/settings.json` file in the project's root directory.

## Claude Desktop

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
