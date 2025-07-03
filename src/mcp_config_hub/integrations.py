import json
import os
import platform
from pathlib import Path
from typing import Dict, Any, Optional
import click
from .diff_utils import generate_config_diff, has_changes


class BaseIntegration:
    """Base class for tool integrations."""
    
    def get_config_path(self) -> Path:
        """Get the configuration file path for this tool."""
        raise NotImplementedError
    
    def read_config(self) -> Dict[str, Any]:
        """Read configuration from the tool's config file."""
        config_path = self.get_config_path()
        if not config_path.exists():
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def write_config(self, config: Dict[str, Any]) -> None:
        """Write configuration to the tool's config file."""
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def sync_from_hub(self, hub_config: Dict[str, Any]) -> None:
        """Sync configuration from MCP Config Hub to this tool."""
        raise NotImplementedError
    
    def sync_from_hub_with_confirmation(self, hub_config: Dict[str, Any], tool_name: str) -> bool:
        """Sync configuration with diff display and user confirmation."""
        current_config = self.read_config()
        
        new_config = current_config.copy()
        self._apply_hub_config(new_config, hub_config)
        
        if not has_changes(current_config, new_config):
            click.echo(f"No changes needed for {tool_name} configuration.")
            return True
        
        diff = generate_config_diff(current_config, new_config, tool_name)
        if diff:
            click.echo(f"\nProposed changes to {tool_name} configuration:")
            click.echo(diff)
        
        if click.confirm(f"\nApply these changes to {tool_name}?"):
            self.write_config(new_config)
            return True
        else:
            click.echo("Changes cancelled.")
            return False
    
    def _apply_hub_config(self, config: Dict[str, Any], hub_config: Dict[str, Any]) -> None:
        """Apply hub configuration to the target config. Override in subclasses."""
        raise NotImplementedError
    
    def sync_to_hub(self) -> Dict[str, Any]:
        """Sync configuration from this tool to MCP Config Hub format."""
        raise NotImplementedError


class VSCodeIntegration(BaseIntegration):
    """Integration with VSCode MCP server settings."""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_config_path(self) -> Path:
        """Get VSCode user settings path."""
        if self.system == "Darwin":
            base = Path.home() / "Library" / "Application Support" / "Code" / "User"
        elif self.system == "Windows":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "Code" / "User"
        else:
            base = Path.home() / ".config" / "Code" / "User"
        
        return base / "settings.json"
    
    def get_workspace_config_path(self) -> Path:
        """Get VSCode workspace MCP config path."""
        return Path.cwd() / ".vscode" / "mcp.json"
    
    def read_config(self) -> Dict[str, Any]:
        """Read configuration from VSCode settings, preferring workspace over user."""
        workspace_config_path = self.get_workspace_config_path()
        if workspace_config_path.exists():
            try:
                with open(workspace_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        user_config = super().read_config()
        return user_config.get("mcp", {})
    
    def write_config(self, config: Dict[str, Any]) -> None:
        """Write configuration to VSCode workspace mcp.json."""
        workspace_config_path = self.get_workspace_config_path()
        workspace_config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(workspace_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def sync_from_hub(self, hub_config: Dict[str, Any]) -> None:
        """Sync MCP servers to VSCode workspace config."""
        if "mcpServers" in hub_config:
            vscode_config = {"servers": hub_config["mcpServers"]}
            self.write_config(vscode_config)
    
    def _apply_hub_config(self, config: Dict[str, Any], hub_config: Dict[str, Any]) -> None:
        """Apply hub configuration to VSCode MCP config."""
        if "mcpServers" in hub_config:
            config["servers"] = hub_config["mcpServers"]
    
    def sync_to_hub(self) -> Dict[str, Any]:
        """Extract MCP configuration from VSCode settings."""
        vscode_config = self.read_config()
        
        if "servers" in vscode_config:
            return {"mcpServers": vscode_config["servers"]}
        
        return {"mcpServers": {}}


class ClaudeDesktopIntegration(BaseIntegration):
    """Integration with Claude Desktop configuration."""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_config_path(self) -> Path:
        """Get Claude Desktop config path."""
        if self.system == "Darwin":
            base = Path.home() / "Library" / "Application Support" / "Claude"
        elif self.system == "Windows":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "Claude"
        else:
            base = Path.home() / ".config" / "Claude"
        
        return base / "claude_desktop_config.json"
    
    def sync_from_hub(self, hub_config: Dict[str, Any]) -> None:
        """Sync MCP servers to Claude Desktop config."""
        claude_config = self.read_config()
        
        if "mcpServers" in hub_config:
            claude_config["mcpServers"] = hub_config["mcpServers"]
        
        self.write_config(claude_config)
    
    def _apply_hub_config(self, config: Dict[str, Any], hub_config: Dict[str, Any]) -> None:
        """Apply hub configuration to Claude Desktop config."""
        if "mcpServers" in hub_config:
            config["mcpServers"] = hub_config["mcpServers"]
    
    def sync_to_hub(self) -> Dict[str, Any]:
        """Extract MCP configuration from Claude Desktop config."""
        claude_config = self.read_config()
        
        if "mcpServers" in claude_config:
            return {"mcpServers": claude_config["mcpServers"]}
        
        return {"mcpServers": {}}




def get_integration(tool_name: str) -> BaseIntegration:
    """Get integration instance for the specified tool."""
    integrations = {
        'vscode': VSCodeIntegration,
        'claude': ClaudeDesktopIntegration,
    }
    
    if tool_name not in integrations:
        raise ValueError(f"Unsupported tool: {tool_name}")
    
    return integrations[tool_name]()
