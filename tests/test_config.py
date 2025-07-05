from mcp_config_hub.config import ConfigManager


class DummyStorage:
    def __init__(self):
        self.data = {"user": {}, "workspace": {}, "merged": {}}

    def load_config(self, scope):
        return self.data.get(scope, {})

    def save_config(self, config, scope):
        self.data[scope] = config


def test_set_and_get():
    cm = ConfigManager(DummyStorage())
    cm.set("foo.bar", 123)
    assert cm.get("foo.bar", scope="user") == 123


def test_delete():
    cm = ConfigManager(DummyStorage())
    cm.set("foo.bar", 123)
    assert cm.delete("foo.bar")
    assert cm.get("foo.bar") is None
    assert not cm.delete("foo.bar")


def test_get_nested():
    cm = ConfigManager(DummyStorage())
    cm.storage.data["user"] = {"a": {"b": {"c": 1}}}
    assert cm.get("a.b.c") == 1


def test_set_nested():
    cm = ConfigManager(DummyStorage())
    cm.set("a.b.c", 42)
    assert cm.get("a.b.c", scope="user") == 42
