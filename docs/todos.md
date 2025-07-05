# TODOs

## Issue #15: Add default prompt setting

- [ ] **Research**: Investigate how each target application (VSCode, Claude Desktop, etc.) stores and uses default prompts.
- [ ] **Update Documentation**: Update `README.md` and documents under the `docs` directory.
- [ ] **Update `config.py`**: Add a new field (e.g., `default_prompt`) to the configuration data structure.
- [ ] **Update `cli.py`**: Add a new command to set/update the `default_prompt` (e.g., `mcp-config-hub set-prompt "..."`).
- [ ] **Update `integrations.py`**: Modify the logic to include the `default_prompt` in the generated configurations for each application.
- [ ] **Add Tests**: Implement tests to verify the new feature.