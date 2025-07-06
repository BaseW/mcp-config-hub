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
