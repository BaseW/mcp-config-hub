import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union


class ConfigManager:
    """Manages hierarchical MCP server configurations."""
    
    def __init__(self, storage_manager):
        self.storage = storage_manager
    
    def get(self, key: str, scope: str = "merged") -> Any:
        """Get configuration value by key with dot notation."""
        if scope == "merged":
            config = self._get_merged_config()
        else:
            config = self.storage.load_config(scope)
        
        return self._get_nested_value(config, key)
    
    def set(self, key: str, value: Any, scope: str = "user") -> None:
        """Set configuration value by key with dot notation."""
        config = self.storage.load_config(scope)
        self._set_nested_value(config, key, value)
        self.storage.save_config(config, scope)
    
    def list_all(self, scope: str = "merged") -> Dict[str, Any]:
        """List all configuration values."""
        if scope == "merged":
            return self._get_merged_config()
        else:
            return self.storage.load_config(scope)
    
    def _get_merged_config(self) -> Dict[str, Any]:
        """Get merged configuration with proper precedence."""
        global_config = self.storage.load_config("global")
        user_config = self.storage.load_config("user")
        project_config = self.storage.load_config("project")
        
        merged = {}
        self._deep_merge(merged, global_config)
        self._deep_merge(merged, user_config)
        self._deep_merge(merged, project_config)
        
        return merged
    
    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Deep merge source into target dictionary."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def _get_nested_value(self, config: Dict[str, Any], key: str) -> Any:
        """Get nested value using dot notation."""
        keys = key.split('.')
        current = config
        
        for k in keys:
            if not isinstance(current, dict) or k not in current:
                return None
            current = current[k]
        
        return current
    
    def _set_nested_value(self, config: Dict[str, Any], key: str, value: Any) -> None:
        """Set nested value using dot notation."""
        keys = key.split('.')
        current = config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            elif not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        try:
            parsed_value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            parsed_value = value
        
        current[keys[-1]] = parsed_value
