import platform
from pathlib import Path

import pytest

from mcp_config_hub.integrations import (
    ClaudeDesktopIntegration,
    CursorIntegration,
    GeminiIntegration,
    VSCodeIntegration,
    WindsurfIntegration,
    ClaudeCodeIntegration, # Import the new integration
)


def test_vscode_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = VSCodeIntegration()
    config = {"servers": {"foo": "bar"}}
    # Write config
    integration.write_config(config)
    # Read config
    read = integration.read_config()
    assert read["servers"] == {"foo": "bar"}
    # sync_to_hub
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


def test_vscode_prompt_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    integration = VSCodeIntegration()
    prompt_content = "Test VSCode prompt."
    integration._apply_prompt_config(prompt_content)

    copilot_instructions_path = tmp_path / ".github" / "copilot-instructions.md"
    assert copilot_instructions_path.exists()
    with open(copilot_instructions_path, "r", encoding="utf-8") as f:
        assert f.read() == prompt_content

    hub_config = integration.sync_to_hub()
    assert hub_config["default_prompt"] == prompt_content


def test_claude_desktop_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = ClaudeDesktopIntegration()
    config = {"mcpServers": {"foo": "bar"}}
    integration.write_config(config)
    read = integration.read_config()
    assert read["mcpServers"] == {"foo": "bar"}
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


def test_cursor_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = CursorIntegration()
    config = {"mcpServers": {"foo": "bar"}}
    integration.write_config(config)
    read = integration.read_config()
    assert read["mcpServers"] == {"foo": "bar"}
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


def test_cursor_prompt_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    integration = CursorIntegration()
    prompt_content = "Test Cursor prompt."
    integration._apply_hub_config({}, {"default_prompt": prompt_content})

    cursor_rules_path = tmp_path / ".cursor" / "rules" / "default_prompt.txt"
    assert cursor_rules_path.exists()
    with open(cursor_rules_path, "r", encoding="utf-8") as f:
        assert f.read() == prompt_content

    hub_config = integration.sync_to_hub()
    assert hub_config["default_prompt"] == prompt_content

    # Test deletion
    integration._apply_hub_config({}, {})
    assert not cursor_rules_path.exists()


def test_windsurf_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = WindsurfIntegration()
    config = {"mcpServers": {"foo": "bar"}}
    integration.write_config(config)
    read = integration.read_config()
    assert read["mcpServers"] == {"foo": "bar"}
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


def test_windsurf_prompt_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    integration = WindsurfIntegration()
    prompt_content = "Test Windsurf prompt."
    integration._apply_hub_config({}, {"default_prompt": prompt_content})

    windsurf_rules_path = tmp_path / ".windsurfrules"
    assert windsurf_rules_path.exists()
    with open(windsurf_rules_path, "r", encoding="utf-8") as f:
        assert f.read() == prompt_content

    hub_config = integration.sync_to_hub()
    assert hub_config["default_prompt"] == prompt_content

    # Test deletion
    integration._apply_hub_config({}, {})
    assert not windsurf_rules_path.exists()


def test_gemini_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = GeminiIntegration()
    config = {"mcpServers": {"foo": "bar"}}
    integration.write_config(config)
    read = integration.read_config()
    assert read["mcpServers"] == {"foo": "bar"}
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


def test_gemini_prompt_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    integration = GeminiIntegration()
    prompt_content = "Test Gemini prompt."
    integration._apply_hub_config({}, {"default_prompt": prompt_content})

    gemini_md_path = tmp_path / "GEMINI.md"
    assert gemini_md_path.exists()
    with open(gemini_md_path, "r", encoding="utf-8") as f:
        assert f.read() == prompt_content

    hub_config = integration.sync_to_hub()
    assert hub_config["default_prompt"] == prompt_content

    # Test deletion
    integration._apply_hub_config({}, {})
    assert not gemini_md_path.exists()


def test_claude_code_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = ClaudeCodeIntegration()
    config = {"mcpServers": {"foo": "bar"}}
    integration.write_config(config)
    read = integration.read_config()
    assert read["mcpServers"] == {"foo": "bar"}
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


def test_claude_code_prompt_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    integration = ClaudeCodeIntegration()
    prompt_content = "Test Claude Code prompt."
    integration._apply_hub_config({}, {"default_prompt": prompt_content})

    claude_md_path = tmp_path / "CLAUDE.md"
    assert claude_md_path.exists()
    with open(claude_md_path, "r", encoding="utf-8") as f:
        assert f.read() == prompt_content

    hub_config = integration.sync_to_hub()
    assert hub_config["default_prompt"] == prompt_content

    # Test deletion
    integration._apply_hub_config({}, {})
    assert not claude_md_path.exists()


def test_vscode_apply_hub_config(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = VSCodeIntegration()
    config = {}
    hub = {"mcpServers": {"a": 1}}
    integration._apply_hub_config(config, hub)
    assert config["servers"] == {"a": 1}


def test_claude_apply_hub_config(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = ClaudeDesktopIntegration()
    config = {}
    hub = {"mcpServers": {"a": 1}}
    integration._apply_hub_config(config, hub)
    assert config["mcpServers"] == {"a": 1}


def test_cursor_apply_hub_config(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = CursorIntegration()
    config = {}
    hub = {"mcpServers": {"a": 1}}
    integration._apply_hub_config(config, hub)
    assert config["mcpServers"] == {"a": 1}


def test_windsurf_apply_hub_config(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = WindsurfIntegration()
    config = {}
    hub = {"mcpServers": {"a": 1}}
    integration._apply_hub_config(config, hub)
    assert config["mcpServers"] == {"a": 1}


def test_gemini_apply_hub_config(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = GeminiIntegration()
    config = {}
    hub = {"mcpServers": {"a": 1}}
    integration._apply_hub_config(config, hub)
    assert config["mcpServers"] == {"a": 1}


def test_claude_code_apply_hub_config(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = ClaudeCodeIntegration()
    config = {}
    hub = {"mcpServers": {"a": 1}}
    integration._apply_hub_config(config, hub)
    assert config["mcpServers"] == {"a": 1}


def test_get_integration():
    from mcp_config_hub.integrations import get_integration

    assert isinstance(get_integration("vscode"), VSCodeIntegration)
    assert isinstance(get_integration("claude"), ClaudeDesktopIntegration)
    assert isinstance(get_integration("cursor"), CursorIntegration)
    assert isinstance(get_integration("windsurf"), WindsurfIntegration)
    assert isinstance(get_integration("gemini"), GeminiIntegration)
    assert isinstance(get_integration("claude_code"), ClaudeCodeIntegration)
    with pytest.raises(ValueError):
        get_integration("unknown")


def test_get_all_integrations():
    from mcp_config_hub.integrations import get_all_integrations

    integrations = get_all_integrations()
    assert isinstance(integrations["vscode"], VSCodeIntegration)
    assert isinstance(integrations["claude"], ClaudeDesktopIntegration)
    assert isinstance(integrations["cursor"], CursorIntegration)
    assert isinstance(integrations["windsurf"], WindsurfIntegration)
    assert isinstance(integrations["gemini"], GeminiIntegration)
    assert isinstance(integrations["claude_code"], ClaudeCodeIntegration)
    assert len(integrations) == 6
