import pytest

from mcp_config_hub.formatters import JSONFormatter, TOMLFormatter, YAMLFormatter


def test_json_formatter():
    f = JSONFormatter()
    data = {"a": 1}
    out = f.format(data)
    assert '"a": 1' in out


def test_yaml_formatter():
    f = YAMLFormatter()
    data = {"a": 1}
    out = f.format(data)
    assert "a: 1" in out or "a: 1\n" in out


def test_toml_formatter():
    f = TOMLFormatter()
    data = {"a": 1}
    out = f.format(data)
    assert "a = 1" in out or "a = 1\n" in out


def test_yaml_formatter_error():
    # PyYAMLが未インストール時の例外テスト
    import sys

    orig_yaml = sys.modules.get("yaml")
    sys.modules["yaml"] = None
    try:
        f = YAMLFormatter()
        with pytest.raises(RuntimeError):
            f.format({"a": 1})
    finally:
        if orig_yaml is not None:
            sys.modules["yaml"] = orig_yaml
        else:
            del sys.modules["yaml"]


def test_toml_formatter_error():
    # tomli_wが未インストール時の例外テスト
    import sys

    orig_tomli_w = sys.modules.get("tomli_w")
    sys.modules["tomli_w"] = None
    try:
        f = TOMLFormatter()
        with pytest.raises(RuntimeError):
            f.format({"a": 1})
    finally:
        if orig_tomli_w is not None:
            sys.modules["tomli_w"] = orig_tomli_w
        else:
            del sys.modules["tomli_w"]
