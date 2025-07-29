"""MCP template plugin - the original/default template."""

from pathlib import Path
from typing import Any, Dict, List

from ..base import TemplatePlugin


class MCPTemplatePlugin(TemplatePlugin):
    """Original MCP server template plugin."""

    def __init__(self) -> None:
        """Initialize the MCP template plugin."""
        super().__init__(
            name="mcp",
            description="Standard MCP server template with FASTMCP framework",
            version="1.0.0",
        )

    def get_template_path(self) -> Path:
        """Get the path to the cookiecutter template directory.

        Returns:
            Path to the template directory containing cookiecutter.json
        """
        # Point to the existing template directory
        return Path(__file__).parent.parent.parent / "template"

    def get_default_context(self) -> Dict[str, Any]:
        """Get default context variables for the template.

        Returns:
            Dictionary of default template variables
        """
        return {
            "project_name": "My MCP Server",
            "project_slug": "my_mcp_server",
            "project_description": "A Model Context Protocol server built with FASTMCP",
            "author_name": "Your Name",
            "author_email": "your.email@example.com",
            "github_username": "yourusername",
            "version": "0.1.0",
            "python_version": "3.11",
            "use_docker": "y",
            "use_github_actions": "y",
            "use_pre_commit": "y",
            "license": "MIT",
            "include_examples": "y",
            "server_type": "full",
        }

    def get_supported_features(self) -> List[str]:
        """Get list of features supported by this template.

        Returns:
            List of feature names
        """
        return [
            "docker",
            "github_actions",
            "pre_commit",
            "testing",
            "documentation",
            "multiple_licenses",
            "server_types",
            "examples",
        ]

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate the provided context for this template.

        Args:
            context: Template context variables

        Returns:
            True if context is valid, False otherwise
        """
        required_fields = ["project_name", "author_name", "author_email"]
        return all(field in context and context[field] for field in required_fields)

    def pre_generate_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before project generation.

        Args:
            context: Template context variables

        Returns:
            Modified context variables
        """
        # Ensure project_slug is properly formatted based on project_name
        if "project_name" in context:
            project_slug = (
                context["project_name"].lower().replace(" ", "_").replace("-", "_")
            )
            context["project_slug"] = project_slug

        return context

    def post_generate_hook(self, project_path: Path, context: Dict[str, Any]) -> None:
        """Hook called after project generation.

        Args:
            project_path: Path to the generated project
            context: Template context variables used during generation
        """
        # Could add post-generation steps like:
        # - Initialize git repository
        # - Set up virtual environment
        # - Install pre-commit hooks
        pass
