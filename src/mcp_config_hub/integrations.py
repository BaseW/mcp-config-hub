import json
import os
import platform
from pathlib import Path
from typing import Any, Dict

import click

from .diff_utils import generate_config_diff, has_changes


class BaseIntegration:
    """Base class for tool integrations."""

    def get_config_path(self) -> Path:
        """Get the configuration file path for this tool."""
        raise NotImplementedError

    def read_config(self) -> dict[str, Any]:
        """Read configuration from the tool's config file."""
        config_path = self.get_config_path()
        if not config_path.exists():
            return {}

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def write_config(self, config: dict[str, Any]) -> None:
        """Write configuration to the tool's config file."""
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def sync_from_hub(self, hub_config: dict[str, Any]) -> None:
        """Sync configuration from MCP Config Hub to this tool."""
        raise NotImplementedError

    def sync_from_hub_with_confirmation(
        self, hub_config: dict[str, Any], tool_name: str
    ) -> bool:
        """Sync configuration with diff display and user confirmation."""
        current_config = self.read_config()

        new_config = current_config.copy()
        self._apply_hub_config(new_config, hub_config)

        if not has_changes(current_config, new_config):
            # Check for prompt file changes if applicable
            if tool_name == "VSCode" and "default_prompt" in hub_config:
                copilot_instructions_path = (
                    Path.cwd() / ".github" / "copilot-instructions.md"
                )
                if copilot_instructions_path.exists():
                    with open(copilot_instructions_path, "r", encoding="utf-8") as f:
                        if f.read() == hub_config["default_prompt"]:
                            click.echo(
                                f"No changes needed for {tool_name} configuration."
                            )
                            return True
                else:
                    click.echo(
                        f"Changes needed for {tool_name} configuration (prompt file)."
                    )
                    return False
            elif tool_name == "Cursor" and "default_prompt" in hub_config:
                cursor_rules_path = (
                    Path.cwd() / ".cursor" / "rules" / "default_prompt.txt"
                )
                if cursor_rules_path.exists():
                    with open(cursor_rules_path, "r", encoding="utf-8") as f:
                        if f.read() == hub_config["default_prompt"]:
                            click.echo(
                                f"No changes needed for {tool_name} configuration."
                            )
                            return True
                else:
                    click.echo(
                        f"Changes needed for {tool_name} configuration (prompt file)."
                    )
                    return False
            elif tool_name == "Windsurf" and "default_prompt" in hub_config:
                windsurf_rules_path = Path.cwd() / ".windsurfrules"
                if windsurf_rules_path.exists():
                    with open(windsurf_rules_path, "r", encoding="utf-8") as f:
                        if f.read() == hub_config["default_prompt"]:
                            click.echo(
                                f"No changes needed for {tool_name} configuration."
                            )
                            return True
                else:
                    click.echo(
                        f"Changes needed for {tool_name} configuration (prompt file)."
                    )
                    return False
            elif tool_name == "Gemini CLI" and "default_prompt" in hub_config:
                gemini_md_path = Path.cwd() / "GEMINI.md"
                if gemini_md_path.exists():
                    with open(gemini_md_path, "r", encoding="utf-8") as f:
                        if f.read() == hub_config["default_prompt"]:
                            click.echo(
                                f"No changes needed for {tool_name} configuration."
                            )
                            return True
                else:
                    click.echo(
                        f"Changes needed for {tool_name} configuration (prompt file)."
                    )
                    return False
            elif tool_name == "Claude Code" and "default_prompt" in hub_config:
                claude_md_path = Path.cwd() / "CLAUDE.md"
                if claude_md_path.exists():
                    with open(claude_md_path, "r", encoding="utf-8") as f:
                        if f.read() == hub_config["default_prompt"]:
                            click.echo(
                                f"No changes needed for {tool_name} configuration."
                            )
                            return True
                else:
                    click.echo(
                        f"Changes needed for {tool_name} configuration (prompt file)."
                    )
                    return False
            else:
                click.echo(f"No changes needed for {tool_name} configuration.")
                return True

        diff = generate_config_diff(current_config, new_config, tool_name)
        if diff:
            click.echo(f"\nProposed changes to {tool_name} configuration:")
            click.echo(diff)

        if click.confirm(f"\nApply these changes to {tool_name}?"):
            self.write_config(new_config)
            if "default_prompt" in hub_config:
                self._apply_prompt_config(hub_config["default_prompt"])
            return True
        else:
            click.echo("Changes cancelled.")
            return False

    def _apply_hub_config(
        self, config: Dict[str, Any], hub_config: Dict[str, Any]
    ) -> None:
        """Apply hub configuration to the target config. Override in subclasses."""
        raise NotImplementedError

    def _apply_prompt_config(self, prompt_content: str) -> None:
        """Apply default prompt from hub configuration to the tool's specific prompt setting."""
        pass

    def sync_to_hub(self) -> Dict[str, Any]:
        """Sync configuration from this tool to MCP Config Hub format."""
        raise NotImplementedError


class VSCodeIntegration(BaseIntegration):
    """Integration with VSCode MCP server settings."""

    def __init__(self):
        self.system = platform.system()

    def get_config_path(self) -> Path:
        if self.system == "Darwin":
            base = Path.home() / "Library" / "Application Support" / "Code" / "User"
        elif self.system == "Windows":
            base = (
                Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
                / "Code"
                / "User"
            )
        else:
            base = Path.home() / ".config" / "Code" / "User"

        return base / "settings.json"

    def get_workspace_config_path(self) -> Path:
        return Path.cwd() / ".vscode" / "mcp.json"

    def read_config(self) -> Dict[str, Any]:
        workspace_config_path = self.get_workspace_config_path()
        if workspace_config_path.exists():
            try:
                with open(workspace_config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        user_config = super().read_config()
        return user_config.get("mcp", {})

    def write_config(self, config: Dict[str, Any]) -> None:
        workspace_config_path = self.get_workspace_config_path()
        workspace_config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(workspace_config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _apply_hub_config(
        self, config: Dict[str, Any], hub_config: Dict[str, Any]
    ) -> None:
        if "mcpServers" in hub_config:
            config["servers"] = hub_config["mcpServers"]
        if "default_prompt" in hub_config:
            if "prompts" not in config:
                config["prompts"] = {}
            config["prompts"]["default_prompt"] = hub_config["default_prompt"]

    def _apply_prompt_config(self, prompt_content: str) -> None:
        copilot_dir = Path.cwd() / ".github"
        copilot_dir.mkdir(parents=True, exist_ok=True)
        copilot_instructions_path = copilot_dir / "copilot-instructions.md"
        with open(copilot_instructions_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)

    def sync_to_hub(self) -> Dict[str, Any]:
        vscode_config = self.read_config()
        hub_config: Dict[str, Any] = {"mcpServers": {}}

        if "servers" in vscode_config:
            hub_config["mcpServers"] = vscode_config["servers"]

        copilot_instructions_path = Path.cwd() / ".github" / "copilot-instructions.md"
        if copilot_instructions_path.exists():
            try:
                with open(copilot_instructions_path, "r", encoding="utf-8") as f:
                    hub_config["default_prompt"] = f.read()
            except IOError:
                pass

        return hub_config


class ClaudeDesktopIntegration(BaseIntegration):
    """Integration with Claude Desktop configuration."""

    def __init__(self):
        self.system = platform.system()

    def get_config_path(self) -> Path:
        if self.system == "Darwin":
            base = Path.home() / "Library" / "Application Support" / "Claude"
        elif self.system == "Windows":
            base = (
                Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
                / "Claude"
            )
        else:
            base = Path.home() / ".config" / "Claude"

        return base / "claude_desktop_config.json"

    def _apply_hub_config(
        self, config: Dict[str, Any], hub_config: Dict[str, Any]
    ) -> None:
        if "mcpServers" in hub_config:
            config["mcpServers"] = hub_config["mcpServers"]

    def sync_to_hub(self) -> Dict[str, Any]:
        claude_config = self.read_config()

        if "mcpServers" in claude_config:
            return {"mcpServers": claude_config["mcpServers"]}

        return {"mcpServers": {}}


class CursorIntegration(BaseIntegration):
    """Integration with Cursor MCP server settings."""

    def __init__(self):
        self.system = platform.system()

    def get_config_path(self) -> Path:
        if self.system == "Windows":
            base = Path(os.environ.get("USERPROFILE", Path.home())) / ".cursor"
        else:
            base = Path.home() / ".cursor"
        project_config = Path.cwd() / ".cursor" / "mcp.json"
        if project_config.exists():
            return project_config
        return base / "mcp.json"

    def read_config(self) -> Dict[str, Any]:
        config = super().read_config()
        return config

    def write_config(self, config: Dict[str, Any]) -> None:
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _apply_hub_config(
        self, config: Dict[str, Any], hub_config: Dict[str, Any]
    ) -> None:
        if "mcpServers" in hub_config:
            config["mcpServers"] = hub_config["mcpServers"]
        if "default_prompt" in hub_config:
            self._write_cursor_rules(hub_config["default_prompt"])
        else:
            cursor_rules_path = Path.cwd() / ".cursor" / "rules" / "default_prompt.txt"
            if cursor_rules_path.exists():
                cursor_rules_path.unlink()

    def _write_cursor_rules(self, prompt_content: str) -> None:
        cursor_rules_dir = Path.cwd() / ".cursor" / "rules"
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        cursor_rules_path = cursor_rules_dir / "default_prompt.txt"
        with open(cursor_rules_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)

    def sync_to_hub(self) -> Dict[str, Any]:
        config = self.read_config()
        hub_config: Dict[str, Any] = {"mcpServers": {}}
        if "mcpServers" in config:
            hub_config["mcpServers"] = config["mcpServers"]

        cursor_rules_path = Path.cwd() / ".cursor" / "rules" / "default_prompt.txt"
        if cursor_rules_path.exists():
            try:
                with open(cursor_rules_path, "r", encoding="utf-8") as f:
                    hub_config["default_prompt"] = f.read()
            except IOError:
                pass
        return hub_config


class WindsurfIntegration(BaseIntegration):
    """Integration with Windsurf MCP server settings."""

    def __init__(self):
        self.system = platform.system()

    def get_config_path(self) -> Path:
        if self.system == "Windows":
            base = (
                Path(os.environ.get("USERPROFILE", Path.home()))
                / ".codeium"
                / "windsurf"
            )
        else:
            base = Path.home() / ".codeium" / "windsurf"
        return base / "mcp_config.json"

    def read_config(self) -> Dict[str, Any]:
        config = super().read_config()
        return config

    def write_config(self, config: Dict[str, Any]) -> None:
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _apply_hub_config(
        self, config: Dict[str, Any], hub_config: Dict[str, Any]
    ) -> None:
        if "mcpServers" in hub_config:
            config["mcpServers"] = hub_config["mcpServers"]
        if "default_prompt" in hub_config:
            self._write_windsurf_rules(hub_config["default_prompt"])
        else:
            windsurf_rules_path = Path.cwd() / ".windsurfrules"
            if windsurf_rules_path.exists():
                windsurf_rules_path.unlink()

    def _write_windsurf_rules(self, prompt_content: str) -> None:
        windsurf_rules_path = Path.cwd() / ".windsurfrules"
        with open(windsurf_rules_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)

    def sync_to_hub(self) -> Dict[str, Any]:
        config = self.read_config()
        hub_config: Dict[str, Any] = {"mcpServers": {}}
        if "mcpServers" in config:
            hub_config["mcpServers"] = config["mcpServers"]

        windsurf_rules_path = Path.cwd() / ".windsurfrules"
        if windsurf_rules_path.exists():
            try:
                with open(windsurf_rules_path, "r", encoding="utf-8") as f:
                    hub_config["default_prompt"] = f.read()
            except IOError:
                pass
        return hub_config


class GeminiIntegration(BaseIntegration):
    """Integration with Gemini CLI MCP server settings."""

    def __init__(self):
        self.system = platform.system()

    def get_config_path(self) -> Path:
        project_config = Path.cwd() / ".gemini" / "settings.json"
        if project_config.exists():
            return project_config
        if self.system == "Windows":
            base = Path(os.environ.get("USERPROFILE", Path.home())) / ".gemini"
        else:
            base = Path.home() / ".gemini"
        return base / "settings.json"

    def read_config(self) -> Dict[str, Any]:
        config = super().read_config()
        return config

    def write_config(self, config: Dict[str, Any]) -> None:
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _apply_hub_config(
        self, config: Dict[str, Any], hub_config: Dict[str, Any]
    ) -> None:
        if "mcpServers" in hub_config:
            config["mcpServers"] = hub_config["mcpServers"]
        if "default_prompt" in hub_config:
            self._write_gemini_md(hub_config["default_prompt"])
        else:
            gemini_md_path = Path.cwd() / "GEMINI.md"
            if gemini_md_path.exists():
                gemini_md_path.unlink()

    def _write_gemini_md(self, prompt_content: str) -> None:
        gemini_md_path = Path.cwd() / "GEMINI.md"
        with open(gemini_md_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)

    def sync_to_hub(self) -> Dict[str, Any]:
        config = self.read_config()
        hub_config: Dict[str, Any] = {"mcpServers": {}}
        if "mcpServers" in config:
            hub_config["mcpServers"] = config["mcpServers"]

        gemini_md_path = Path.cwd() / "GEMINI.md"
        if gemini_md_path.exists():
            try:
                with open(gemini_md_path, "r", encoding="utf-8") as f:
                    hub_config["default_prompt"] = f.read()
            except IOError:
                pass
        return hub_config


class ClaudeCodeIntegration(BaseIntegration):
    """Integration with Claude Code CLI settings."""

    def __init__(self):
        self.system = platform.system()

    def get_config_path(self) -> Path:
        # Prioritize project-specific settings.json
        project_config_path = Path.cwd() / ".claude" / "settings.json"
        if project_config_path.exists():
            return project_config_path

        # Then user-specific settings.json
        if self.system == "Windows":
            base = (
                Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
                / "Claude"
            )
        else:
            base = Path.home() / ".claude"
        return base / "settings.json"

    def read_config(self) -> Dict[str, Any]:
        config = super().read_config()
        return config

    def write_config(self, config: Dict[str, Any]) -> None:
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _apply_hub_config(
        self, config: Dict[str, Any], hub_config: Dict[str, Any]
    ) -> None:
        if "mcpServers" in hub_config:
            config["mcpServers"] = hub_config["mcpServers"]
        if "default_prompt" in hub_config:
            self._write_claude_md(hub_config["default_prompt"])
        else:
            claude_md_path = Path.cwd() / "CLAUDE.md"
            if claude_md_path.exists():
                claude_md_path.unlink()

    def _write_claude_md(self, prompt_content: str) -> None:
        claude_md_path = Path.cwd() / "CLAUDE.md"
        with open(claude_md_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)

    def sync_to_hub(self) -> Dict[str, Any]:
        config = self.read_config()
        hub_config: Dict[str, Any] = {"mcpServers": {}}
        if "mcpServers" in config:
            hub_config["mcpServers"] = config["mcpServers"]

        claude_md_path = Path.cwd() / "CLAUDE.md"
        if claude_md_path.exists():
            try:
                with open(claude_md_path, "r", encoding="utf-8") as f:
                    hub_config["default_prompt"] = f.read()
            except IOError:
                pass
        return hub_config


def get_integration(tool_name: str) -> BaseIntegration:
    """Get integration instance for the specified tool."""
    integrations = {
        "vscode": VSCodeIntegration,
        "claude": ClaudeDesktopIntegration,
        "cursor": CursorIntegration,
        "windsurf": WindsurfIntegration,
        "gemini": GeminiIntegration,
        "claude_code": ClaudeCodeIntegration,
    }

    if tool_name not in integrations:
        raise ValueError(f"Unsupported tool: {tool_name}")

    return integrations[tool_name]()


def get_all_integrations() -> Dict[str, BaseIntegration]:
    """Get all available integration instances."""
    return {
        "vscode": VSCodeIntegration(),
        "claude": ClaudeDesktopIntegration(),
        "cursor": CursorIntegration(),
        "windsurf": WindsurfIntegration(),
        "gemini": GeminiIntegration(),
        "claude_code": ClaudeCodeIntegration(),
    }
