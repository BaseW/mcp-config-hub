import json
import os
import platform
from pathlib import Path
from typing import Dict, Any, Optional


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
    
    def sync_to_hub(self) -> Dict[str, Any]:
        """Sync configuration from this tool to MCP Config Hub format."""
        raise NotImplementedError


class VSCodeIntegration(BaseIntegration):
    """Integration with VSCode settings."""
    
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
    
    def sync_from_hub(self, hub_config: Dict[str, Any]) -> None:
        """Sync MCP servers to VSCode settings."""
        vscode_config = self.read_config()
        
        if "mcpServers" in hub_config:
            vscode_config["mcp.servers"] = hub_config["mcpServers"]
        
        self.write_config(vscode_config)
    
    def sync_to_hub(self) -> Dict[str, Any]:
        """Extract MCP configuration from VSCode settings."""
        vscode_config = self.read_config()
        
        if "mcp.servers" in vscode_config:
            return {"mcpServers": vscode_config["mcp.servers"]}
        
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
    
    def sync_to_hub(self) -> Dict[str, Any]:
        """Extract MCP configuration from Claude Desktop config."""
        claude_config = self.read_config()
        
        if "mcpServers" in claude_config:
            return {"mcpServers": claude_config["mcpServers"]}
        
        return {"mcpServers": {}}


class ChatGPTIntegration(BaseIntegration):
    """Integration with ChatGPT configuration."""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_config_path(self) -> Path:
        """Get ChatGPT config path."""
        if self.system == "Darwin":
            base = Path.home() / "Library" / "Application Support" / "ChatGPT"
        elif self.system == "Windows":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "ChatGPT"
        else:
            base = Path.home() / ".config" / "ChatGPT"
        
        return base / "config.json"
    
    def sync_from_hub(self, hub_config: Dict[str, Any]) -> None:
        """Sync MCP servers to ChatGPT config."""
        chatgpt_config = self.read_config()
        
        if "mcpServers" in hub_config:
            chatgpt_config["mcpServers"] = hub_config["mcpServers"]
        
        self.write_config(chatgpt_config)
    
    def sync_to_hub(self) -> Dict[str, Any]:
        """Extract MCP configuration from ChatGPT config."""
        chatgpt_config = self.read_config()
        
        if "mcpServers" in chatgpt_config:
            return {"mcpServers": chatgpt_config["mcpServers"]}
        
        return {"mcpServers": {}}


def get_integration(tool_name: str) -> BaseIntegration:
    """Get integration instance for the specified tool."""
    integrations = {
        'vscode': VSCodeIntegration,
        'claude': ClaudeDesktopIntegration,
        'chatgpt': ChatGPTIntegration,
    }
    
    if tool_name not in integrations:
        raise ValueError(f"Unsupported tool: {tool_name}")
    
    return integrations[tool_name]()
