"""CLI interface for egile-mcp-starter."""

import sys

import click

from .generator import MCPProjectGenerator


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
def main(
    output_dir: str,
    no_input: bool,
    config_file: str,
    default_config: bool,
    verbose: bool,
) -> None:
    """
    Generate a new MCP server project using the FASTMCP framework.

    This tool creates a complete MCP server project structure with:
    - FASTMCP-based server implementation
    - Docker support
    - Testing framework
    - Documentation
    - CI/CD configuration
    """
    try:
        generator = MCPProjectGenerator(
            output_dir=output_dir,
            no_input=no_input,
            config_file=config_file,
            default_config=default_config,
            verbose=verbose,
        )

        project_path = generator.generate()

        if verbose:
            click.echo(
                f"✅ MCP server project generated successfully at: {project_path}"
            )
            click.echo("\n🚀 Next steps:")
            click.echo(f"  cd {project_path}")
            click.echo("  poetry install")
            click.echo("  poetry run pytest")
            click.echo("  poetry run python src/main.py")
            click.echo("\n📚 Alternative commands:")
            click.echo("  poetry shell  # Activate virtual environment")
            click.echo("  poetry add <package>  # Add new dependencies")

        sys.exit(0)

    except Exception as e:
        click.echo(f"❌ Error generating project: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
