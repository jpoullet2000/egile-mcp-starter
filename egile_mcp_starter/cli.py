"""CLI interface for egile-mcp-starter."""

import sys
from typing import List

import click

from .generator import MCPProjectGenerator
from .plugins.registry import get_registry


@click.command()
@click.option(
    "--output-dir",
    "-o",
    default=".",
    help="Output directory for the generated project",
    type=click.Path(file_okay=False, dir_okay=True),
)
@click.option(
    "--no-input",
    is_flag=True,
    help="Don't prompt for parameters and use default values",
)
@click.option("--config-file", help="User configuration file")
@click.option(
    "--default-config",
    is_flag=True,
    help="Use default values for all template variables",
)
@click.option("--verbose", "-v", is_flag=True, help="Print status to stdout")
@click.option(
    "--template",
    "-t",
    default="mcp",
    help="Template to use for project generation",
    type=click.Choice([]),  # Will be populated dynamically
)
@click.option(
    "--list-templates",
    is_flag=True,
    help="List all available templates and exit",
)
def main(
    output_dir: str,
    no_input: bool,
    config_file: str,
    default_config: bool,
    verbose: bool,
    template: str,
    list_templates: bool,
) -> None:
    """
    Generate a new MCP server project using the FASTMCP framework.

    This tool creates a complete MCP server project structure with:
    - FASTMCP-based server implementation
    - Docker support
    - Testing framework
    - Documentation
    - CI/CD configuration

    Multiple templates are available:
    - mcp: Standard MCP server template
    - rag: RAG-enabled server with vector database support
    """
    # Get the registry for template information
    registry = get_registry()

    # Handle list templates option
    if list_templates:
        click.echo("Available templates:")
        for plugin in registry.list_plugins():
            click.echo(f"  {plugin.name}: {plugin.description}")
        return

    # Validate template choice
    if not registry.get_plugin(template):
        available = ", ".join(registry.get_plugin_names())
        click.echo(f"Error: Template '{template}' not found.", err=True)
        click.echo(f"Available templates: {available}", err=True)
        sys.exit(1)

    try:
        generator = MCPProjectGenerator(
            output_dir=output_dir,
            no_input=no_input,
            config_file=config_file,
            default_config=default_config,
            verbose=verbose,
            template=template,
        )

        project_path = generator.generate()

        click.echo("✅ MCP server project generated successfully!")
        click.echo(f"📁 Project location: {project_path}")
        click.echo(f"🚀 Template used: {template}")
        click.echo("")
        click.echo("Next steps:")
        project_name = (
            project_path.name
            if hasattr(project_path, "name")
            else str(project_path).split("/")[-1]
        )
        click.echo(f"  cd {project_name}")
        click.echo("  pip install -e .")
        click.echo("  # Start developing your MCP server!")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


# Dynamically populate template choices
def _get_template_choices() -> List[str]:
    """Get available template choices for CLI."""
    try:
        registry = get_registry()
        return registry.get_plugin_names()
    except Exception:
        return ["mcp"]  # Fallback to default


# Update the template option with dynamic choices
main.params[5].type = click.Choice(_get_template_choices())


if __name__ == "__main__":
    sys.exit(main())
