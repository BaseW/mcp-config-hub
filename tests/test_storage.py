import platform
from mcp_config_hub.storage import StorageManager

def test_get_config_path_user(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    sm = StorageManager()
    path = sm.get_config_path("user")
    assert "Application Support" in str(path)

def test_get_config_path_global(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    sm = StorageManager()
    path = sm.get_config_path("global")
    assert "/etc/mcp-config-hub/config.json" in str(path)

def test_get_config_path_project(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    sm = StorageManager()
    path = sm.get_config_path("project")
    assert ".mcp-config-hub/config.json" in str(path)

def test_invalid_scope():
    sm = StorageManager()
    try:
        sm.get_config_path("invalid")
    except ValueError as e:
        assert "Invalid scope" in str(e)
    else:
        assert False, "ValueError not raised"
