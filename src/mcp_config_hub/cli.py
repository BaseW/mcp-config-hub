import click
import sys
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


@cli.group()
def sync():
    """Sync configurations with external tools."""
    pass


@sync.command()
@click.option('--direction', default='from-hub', 
              type=click.Choice(['from-hub', 'to-hub']),
              help='Sync direction')
def vscode(direction):
    """Sync with VSCode settings."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        integration = get_integration('vscode')
        
        if direction == 'from-hub':
            hub_config = config_manager.list_all('merged')
            integration.sync_from_hub(hub_config)
            click.echo("Synced MCP Config Hub settings to VSCode")
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
def claude(direction):
    """Sync with Claude Desktop configuration."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        integration = get_integration('claude')
        
        if direction == 'from-hub':
            hub_config = config_manager.list_all('merged')
            integration.sync_from_hub(hub_config)
            click.echo("Synced MCP Config Hub settings to Claude Desktop")
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
def chatgpt(direction):
    """Sync with ChatGPT configuration."""
    try:
        storage = StorageManager()
        config_manager = ConfigManager(storage)
        integration = get_integration('chatgpt')
        
        if direction == 'from-hub':
            hub_config = config_manager.list_all('merged')
            integration.sync_from_hub(hub_config)
            click.echo("Synced MCP Config Hub settings to ChatGPT")
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
