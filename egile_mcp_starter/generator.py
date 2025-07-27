"""Project generator for MCP servers using cookiecutter."""

from pathlib import Path
from typing import Any, Dict, Optional

try:
    from cookiecutter.main import cookiecutter  # type: ignore
except ImportError:
    cookiecutter = None


class MCPProjectGenerator:
    """Generator for MCP server projects using the FASTMCP framework."""

    def __init__(
        self,
        output_dir: str = ".",
        no_input: bool = False,
        config_file: Optional[str] = None,
        default_config: bool = False,
        verbose: bool = False,
    ):
        """Initialize the MCP project generator.

        Args:
            output_dir: Directory where the project will be created
            no_input: Skip interactive prompts and use defaults
            config_file: Path to cookiecutter config file
            default_config: Use default configuration values
            verbose: Enable verbose output
        """
        self.output_dir = Path(output_dir).resolve()
        self.no_input = no_input or default_config
        self.config_file = config_file
        self.verbose = verbose

        # Get the template directory
        self.template_dir = Path(__file__).parent / "template"

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

        if self.verbose:
            print(f"🔨 Generating MCP server project in: {self.output_dir}")
            print(f"📁 Using template from: {self.template_dir}")

        try:
            # Use cookiecutter to generate the project
            project_path = cookiecutter(
                str(self.template_dir),
                output_dir=str(self.output_dir),
                no_input=self.no_input,
                config_file=self.config_file,
            )

            return Path(project_path)

        except Exception as e:
            raise Exception(f"Failed to generate MCP server project: {e}") from e

    def get_default_context(self) -> Dict[str, Any]:
        """Get the default context variables for the template.

        Returns:
            Dictionary of default template variables
        """
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
