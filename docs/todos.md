# TODOs

## Issue #15: Add default prompt setting

- [x] **Research**: Investigate how each target application (VSCode, Claude, Cursor, Windsurf, Gemini) stores and uses default prompts.
- [x] **Update `config.py`**: Add a new field (`default_prompt`) to the configuration data structure. (No code changes needed, `ConfigManager` is generic.)
- [x] **Update `cli.py`**: Add a new command to set/update the `default_prompt` (e.g., `mcp-config-hub set-prompt "..."`).
- [x] **Update `integrations.py`**: 
    - [x] Implement logic to manage default prompt files/settings for VSCode (`.github/copilot-instructions.md`).
    - [ ] Implement logic for Claude (via MCP, requires further investigation).
    - [x] Implement logic for Cursor (`.cursor/rules`).
    - [x] Implement logic for Windsurf (`.windsurfrules`).
    - [x] Implement logic for Gemini CLI (`GEMINI.md`).
- [x] **Add Tests**: Implement tests for the new prompt integration for all supported tools.
- [x] **Update Documentation**: Update `README.md` and `docs/configuration_research.md` with details about the new feature and supported applications.

## Issue #19: Enhance Claude AI integration

- [x] **Research**: Investigate Claude Code CLI capabilities and API for programmatic interaction. (Completed with findings on settings.json and MCP server config)
- [x] **Research**: Investigate Claude Code CLI prompt setting methods. (Completed with findings on CLAUDE.md)
- [x] **Implement Claude Code CLI Integration**: Add functionality to `mcp-config-hub` to manage Claude Code CLI's `settings.json` files (user, project, local) for MCP server configurations, and to manage `CLAUDE.md` for default prompt setting.
- [ ] **Enhance Claude Prompt Management**: Explore methods to pass `default_prompt` from `mcp-config-hub` to Claude AI API calls (if applicable via MCP server). This might involve configuring a custom MCP server that accepts prompts.
- [x] **Add Tests**: Write unit and integration tests for new Claude AI integration features.
- [ ] **Update Documentation**: Document the enhanced Claude AI integration and usage.