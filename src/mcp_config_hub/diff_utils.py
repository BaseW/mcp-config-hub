import difflib
import json
from typing import Any, Optional


def generate_config_diff(
    current_config: dict[str, Any], new_config: dict[str, Any], tool_name: str
) -> Optional[str]:
    """Generate a readable diff between current and new configurations."""
    current_json = json.dumps(current_config, indent=2, sort_keys=True)
    new_json = json.dumps(new_config, indent=2, sort_keys=True)

    if current_json == new_json:
        return None

    current_lines = current_json.splitlines(keepends=True)
    new_lines = new_json.splitlines(keepends=True)

    diff = difflib.unified_diff(
        current_lines,
        new_lines,
        fromfile=f"{tool_name} (current)",
        tofile=f"{tool_name} (new)",
        lineterm="",
    )

    return "".join(diff)


def has_changes(current_config: dict[str, Any], new_config: dict[str, Any]) -> bool:
    """Check if there are any changes between configurations."""
    current_json = json.dumps(current_config, indent=2, sort_keys=True)
    new_json = json.dumps(new_config, indent=2, sort_keys=True)
    return current_json != new_json
