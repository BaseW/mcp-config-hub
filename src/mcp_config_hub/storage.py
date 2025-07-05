import json
import os
import platform
from pathlib import Path
from typing import Any


class StorageManager:
    """Manages configuration file storage across different scopes and platforms."""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_config_path(self, scope: str) -> Path:
        """Get configuration file path for the given scope."""
        if scope == "global":
            return self._get_global_path()
        elif scope == "user":
            return self._get_user_path()
        elif scope == "project":
            return self._get_project_path()
        else:
            raise ValueError(f"Invalid scope: {scope}")
    
    def _get_global_path(self) -> Path:
        """Get global configuration path."""
        if self.system == "Windows":
            base = Path(os.environ.get("PROGRAMDATA", "C:\\ProgramData"))
        else:
            base = Path("/etc")
        
        return base / "mcp-config-hub" / "config.json"
    
    def _get_user_path(self) -> Path:
        """Get user configuration path."""
        if self.system == "Darwin":
            base = Path.home() / "Library" / "Application Support"
        elif self.system == "Windows":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        else:
            base = Path.home() / ".config"
        
        return base / "mcp-config-hub" / "config.json"
    
    def _get_project_path(self) -> Path:
        """Get project configuration path."""
        return Path.cwd() / ".mcp-config-hub" / "config.json"
    
    def load_config(self, scope: str) -> dict[str, Any]:
        """Load configuration from the specified scope."""
        config_path = self.get_config_path(scope)
        
        if not config_path.exists():
            return self._get_default_config()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._get_default_config()
    
    def save_config(self, config: dict[str, Any], scope: str) -> None:
        """Save configuration to the specified scope."""
        config_path = self.get_config_path(scope)
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        temp_path = config_path.with_suffix('.tmp')
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            temp_path.replace(config_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise
    
    def _get_default_config(self) -> dict[str, Any]:
        """Get default configuration structure."""
        return {
            "mcpServers": {}
        }
