import click
import sys
import json
from .config import ConfigManager
from .storage import StorageManager
from .formatters import get_formatter
from .integrations import get_integration


@click.group()
@click.version_option()
def cli():
    """MCP Config Hub - Manage MCP server configurations."""
    pass


@cli.command()
@click.argument('key')
@click.option('--format', 'output_format', default='json', 
              type=click.Choice(['json', 'yaml', 'toml']),
              help='Output format')
@click.option('--scope', default='merged', 
              type=click.Choice(['global', 'user', 'project', 'merged']),
              help='Configuration scope')
def get(key, output_format, scope):
    """Get configuration value by key (supports dot notation)."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        
        value = config_manager.get(key, scope)
        
        if value is None:
            click.echo(f"Key '{key}' not found in {scope} configuration", err=True)
            sys.exit(1)
        
        formatter = get_formatter(output_format)
        click.echo(formatter.format(value))
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('key')
@click.argument('value')
@click.option('--scope', default='user', 
              type=click.Choice(['global', 'user', 'project']),
              help='Configuration scope')
def set(key, value, scope):
    """Set configuration value by key (supports dot notation)."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        
        config_manager.set(key, value, scope)
        click.echo(f"Set {key} = {value} in {scope} configuration")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--format', 'output_format', default='json', 
              type=click.Choice(['json', 'yaml', 'toml']),
              help='Output format')
@click.option('--scope', default='merged', 
              type=click.Choice(['global', 'user', 'project', 'merged']),
              help='Configuration scope')
def list(output_format, scope):
    """List all configuration values."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        
        config = config_manager.list_all(scope)
        
        formatter = get_formatter(output_format)
        click.echo(formatter.format(config))
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('key')
@click.option('--scope', default='user', 
              type=click.Choice(['global', 'user', 'project']),
              help='Configuration scope')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def delete(key, scope, force):
    """Delete configuration value by key (supports dot notation)."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        
        current_config = config_manager.list_all(scope)
        # 仮想的に削除後の設定を作成
        import copy
        new_config = copy.deepcopy(current_config)
        keys = key.split('.')
        current = new_config
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current = None
                break
            current = current[k]
        if current is not None and keys[-1] in current:
            del current[keys[-1]]
        else:
            click.echo(f"Key '{key}' not found in {scope} configuration", err=True)
            sys.exit(1)
        from .diff_utils import generate_config_diff
        diff = generate_config_diff(current_config, new_config, f"{scope} config")
        if diff:
            click.echo(diff)
        else:
            click.echo('No difference found.')
        if not force:
            c = click.confirm(f"Delete '{key}' from {scope} configuration?", default=False)
            if not c:
                click.echo("Delete cancelled by user")
                sys.exit(0)
        removed = config_manager.delete(key, scope)
        if removed:
            click.echo(f"Deleted {key} from {scope} configuration")
        else:
            click.echo(f"Key '{key}' not found in {scope} configuration", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def sync():
    """Sync configurations with external tools."""
    pass


@sync.command()
@click.option('--direction', default='from-hub', 
              type=click.Choice(['from-hub', 'to-hub']),
              help='Sync direction')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def vscode(direction, force):
    """Sync with VSCode settings."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        integration = get_integration('vscode')
        
        if direction == 'from-hub':
            hub_config = config_manager.list_all('merged')
            if force:
                integration.sync_from_hub(hub_config)
                click.echo("Synced MCP Config Hub settings to VSCode")
            else:
                success = integration.sync_from_hub_with_confirmation(hub_config, 'VSCode')
                if success:
                    click.echo("Synced MCP Config Hub settings to VSCode")
                else:
                    click.echo("Sync cancelled by user")
        else:
            hub_config = integration.sync_to_hub()
            for key, value in hub_config.get('mcpServers', {}).items():
                config_manager.set(f'mcpServers.{key}', value, 'user')
            click.echo("Synced VSCode settings to MCP Config Hub")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@sync.command()
@click.option('--direction', default='from-hub', 
              type=click.Choice(['from-hub', 'to-hub']),
              help='Sync direction')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def claude(direction, force):
    """Sync with Claude Desktop configuration."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        integration = get_integration('claude')
        
        if direction == 'from-hub':
            hub_config = config_manager.list_all('merged')
            if force:
                integration.sync_from_hub(hub_config)
                click.echo("Synced MCP Config Hub settings to Claude Desktop")
            else:
                success = integration.sync_from_hub_with_confirmation(hub_config, 'Claude Desktop')
                if success:
                    click.echo("Synced MCP Config Hub settings to Claude Desktop")
                else:
                    click.echo("Sync cancelled by user")
        else:
            hub_config = integration.sync_to_hub()
            for key, value in hub_config.get('mcpServers', {}).items():
                config_manager.set(f'mcpServers.{key}', value, 'user')
            click.echo("Synced Claude Desktop settings to MCP Config Hub")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@sync.command()
@click.option('--direction', default='from-hub', 
              type=click.Choice(['from-hub', 'to-hub']),
              help='Sync direction')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def chatgpt(direction, force):
    """Sync with ChatGPT configuration."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        integration = get_integration('chatgpt')
        
        if direction == 'from-hub':
            hub_config = config_manager.list_all('merged')
            if force:
                integration.sync_from_hub(hub_config)
                click.echo("Synced MCP Config Hub settings to ChatGPT")
            else:
                success = integration.sync_from_hub_with_confirmation(hub_config, 'ChatGPT')
                if success:
                    click.echo("Synced MCP Config Hub settings to ChatGPT")
                else:
                    click.echo("Sync cancelled by user")
        else:
            hub_config = integration.sync_to_hub()
            for key, value in hub_config.get('mcpServers', {}).items():
                config_manager.set(f'mcpServers.{key}', value, 'user')
            click.echo("Synced ChatGPT settings to MCP Config Hub")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
