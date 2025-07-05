import platform

import pytest

from mcp_config_hub.integrations import (
    ClaudeDesktopIntegration,
    CursorIntegration,
    GeminiIntegration,
    VSCodeIntegration,
    WindsurfIntegration,
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


def test_windsurf_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = WindsurfIntegration()
    config = {"mcpServers": {"foo": "bar"}}
    integration.write_config(config)
    read = integration.read_config()
    assert read["mcpServers"] == {"foo": "bar"}
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


def test_gemini_integration_read_write(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    integration = GeminiIntegration()
    config = {"mcpServers": {"foo": "bar"}}
    integration.write_config(config)
    read = integration.read_config()
    assert read["mcpServers"] == {"foo": "bar"}
    hub = integration.sync_to_hub()
    assert hub["mcpServers"] == {"foo": "bar"}


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


def test_get_integration():
    from mcp_config_hub.integrations import get_integration

    assert isinstance(get_integration("vscode"), VSCodeIntegration)
    assert isinstance(get_integration("claude"), ClaudeDesktopIntegration)
    assert isinstance(get_integration("cursor"), CursorIntegration)
    assert isinstance(get_integration("windsurf"), WindsurfIntegration)
    assert isinstance(get_integration("gemini"), GeminiIntegration)
    with pytest.raises(ValueError):
        get_integration("unknown")
