import json
import sys
from typing import Any

# NOTE: mypyの型エラー回避のため、try-import内でのみyaml_modを定義
try:
    import yaml as yaml_mod
except ImportError:
    yaml_mod = None  # type: ignore

tomllib: Any = None
tomli_w: Any = None
try:
    if sys.version_info >= (3, 11):
        import tomllib

        import tomli_w
    else:
        import importlib.util

        if importlib.util.find_spec("tomli") is not None:
            import tomli as _tomli

            tomllib = _tomli
        if importlib.util.find_spec("tomli_w") is not None:
            import tomli_w as _tomli_w

            tomli_w = _tomli_w
except ImportError:
    pass


class BaseFormatter:
    """Base class for output formatters."""

    def format(self, data: Any) -> str:
        """Format data to string representation."""
        raise NotImplementedError


class JSONFormatter(BaseFormatter):
    """JSON output formatter."""

    def format(self, data: Any) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False)


class YAMLFormatter(BaseFormatter):
    """YAML output formatter."""

    def format(self, data: Any) -> str:
        if yaml_mod is None:
            raise RuntimeError(
                "PyYAML is not installed. Install with: pip install pyyaml"
            )
        return yaml_mod.dump(data, default_flow_style=False, allow_unicode=True)


class TOMLFormatter(BaseFormatter):
    """TOML output formatter."""

    def format(self, data: Any) -> str:
        if tomli_w is None:
            raise RuntimeError(
                "tomli-w is not installed. Install with: pip install tomli-w"
            )
        return tomli_w.dumps(data)


def get_formatter(format_type: str) -> BaseFormatter:
    """Get formatter instance for the specified format type."""
    formatters = {
        "json": JSONFormatter,
        "yaml": YAMLFormatter,
        "toml": TOMLFormatter,
    }

    if format_type not in formatters:
        raise ValueError(f"Unsupported format: {format_type}")

    return formatters[format_type]()
