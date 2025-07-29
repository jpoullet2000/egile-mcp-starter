"""Project generator for MCP servers using cookiecutter."""

from pathlib import Path
from typing import Any, Dict, Optional

try:
    from cookiecutter.main import cookiecutter  # type: ignore
except ImportError:
    cookiecutter = None

from .plugins.registry import get_registry


class MCPProjectGenerator:
    """Generator for MCP server projects using the FASTMCP framework."""

    def __init__(
        self,
        output_dir: str = ".",
        no_input: bool = False,
        config_file: Optional[str] = None,
        default_config: bool = False,
        verbose: bool = False,
        template: str = "mcp",
    ):
        """Initialize the MCP project generator.

        Args:
            output_dir: Directory where the project will be created
            no_input: Skip interactive prompts and use defaults
            config_file: Path to cookiecutter config file
            default_config: Use default configuration values
            verbose: Enable verbose output
            template: Name of the template to use (default: "mcp")
        """
        self.output_dir = Path(output_dir).resolve()
        self.no_input = no_input or default_config
        self.config_file = config_file
        self.verbose = verbose
        self.template_name = template

        # Get the template registry
        self.registry = get_registry()

        # Validate template exists
        if not self.registry.get_plugin(template):
            available = ", ".join(self.registry.get_plugin_names())
            raise ValueError(
                f"Template '{template}' not found. Available templates: {available}"
            )

    def generate(self) -> Path:
        """Generate a new MCP server project.

        Returns:
            Path to the generated project directory

        Raises:
            Exception: If project generation fails
        """
        if cookiecutter is None:
            raise Exception(
                "cookiecutter is not installed. Please install it with: "
                "pip install cookiecutter"
            )

        # Get the template plugin
        plugin = self.registry.get_plugin(self.template_name)
        if not plugin:
            raise Exception(f"Template '{self.template_name}' not found")

        template_dir = plugin.get_template_path()

        if self.verbose:
            print(f"🔨 Generating MCP server project in: {self.output_dir}")
            print(f"📁 Using template: {plugin.name} ({plugin.description})")
            print(f"📂 Template directory: {template_dir}")

        try:
            # Get default context from plugin
            default_context = plugin.get_default_context()

            # Apply pre-generation hook
            if not self.no_input:
                # In interactive mode, cookiecutter will handle the prompts
                context = default_context
            else:
                # In non-interactive mode, use defaults
                context = default_context

            context = plugin.pre_generate_hook(context)

            # Use cookiecutter to generate the project
            if self.no_input:
                project_path = cookiecutter(
                    str(template_dir),
                    output_dir=str(self.output_dir),
                    no_input=True,
                    extra_context=context,
                    config_file=self.config_file,
                )
            else:
                project_path = cookiecutter(
                    str(template_dir),
                    output_dir=str(self.output_dir),
                    no_input=False,
                    config_file=self.config_file,
                )

            project_path_obj = Path(project_path)

            # Apply post-generation hook
            plugin.post_generate_hook(project_path_obj, context)

            return project_path_obj

        except Exception as e:
            raise Exception(f"Failed to generate MCP server project: {e}") from e

    def get_default_context(self) -> Dict[str, Any]:
        """Get the default context variables for the template.

        Returns:
            Dictionary of default template variables
        """
        plugin = self.registry.get_plugin(self.template_name)
        if plugin:
            return plugin.get_default_context()

        # Fallback to original defaults
        return {
            "project_name": "my-mcp-server",
            "project_slug": "my_mcp_server",
            "project_description": "A Model Context Protocol server built with FASTMCP",
            "author_name": "Your Name",
            "author_email": "your.email@example.com",
            "version": "0.1.0",
            "python_version": "3.11",
            "use_docker": "y",
            "use_github_actions": "y",
            "use_pre_commit": "y",
            "license": "MIT",
        }

    def list_available_templates(self) -> Dict[str, str]:
        """List all available templates.

        Returns:
            Dictionary mapping template names to descriptions
        """
        return {
            plugin.name: plugin.description for plugin in self.registry.list_plugins()
        }
