import json
import sys
from typing import Any, Dict

try:
    import yaml
except ImportError:
    yaml = None

try:
    if sys.version_info >= (3, 11):
        import tomllib
        import tomli_w
    else:
        import tomli as tomllib
        import tomli_w
except ImportError:
    tomllib = None
    tomli_w = None


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
        if yaml is None:
            raise RuntimeError("PyYAML is not installed. Install with: pip install pyyaml")
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)


class TOMLFormatter(BaseFormatter):
    """TOML output formatter."""
    
    def format(self, data: Any) -> str:
        if tomli_w is None:
            raise RuntimeError("tomli-w is not installed. Install with: pip install tomli-w")
        return tomli_w.dumps(data)


def get_formatter(format_type: str) -> BaseFormatter:
    """Get formatter instance for the specified format type."""
    formatters = {
        'json': JSONFormatter,
        'yaml': YAMLFormatter,
        'toml': TOMLFormatter,
    }
    
    if format_type not in formatters:
        raise ValueError(f"Unsupported format: {format_type}")
    
    return formatters[format_type]()
