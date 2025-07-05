import sys
import pytest
from mcp_config_hub.formatters import JSONFormatter, YAMLFormatter, TOMLFormatter

def test_json_formatter():
    f = JSONFormatter()
    data = {"a": 1}
    out = f.format(data)
    assert "\"a\": 1" in out

def test_yaml_formatter():
    f = YAMLFormatter()
    data = {"a": 1}
    out = f.format(data)
    assert "a: 1" in out or "a: 1\n" in out

def test_toml_formatter():
    f = TOMLFormatter()
    data = {"a": 1}
    out = f.format(data)
    assert "a = 1" in out

def test_yaml_formatter_importerror(monkeypatch):
    import mcp_config_hub.formatters as fmt
    monkeypatch.setattr(fmt, "yaml", None)
    f = fmt.YAMLFormatter()
    with pytest.raises(RuntimeError):
        f.format({"a": 1})

def test_toml_formatter_importerror(monkeypatch):
    import mcp_config_hub.formatters as fmt
    monkeypatch.setattr(fmt, "tomli_w", None)
    f = fmt.TOMLFormatter()
    with pytest.raises(RuntimeError):
        f.format({"a": 1})
