"""Base template plugin interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class TemplatePlugin(ABC):
    """Base class for template plugins."""

    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        """Initialize the template plugin.

        Args:
            name: Unique name identifier for the template
            description: Human-readable description of the template
            version: Template version
        """
        self.name = name
        self.description = description
        self.version = version

    @abstractmethod
    def get_template_path(self) -> Path:
        """Get the path to the cookiecutter template directory.

        Returns:
            Path to the template directory containing cookiecutter.json
        """
        pass

    @abstractmethod
    def get_default_context(self) -> Dict[str, Any]:
        """Get default context variables for the template.

        Returns:
            Dictionary of default template variables
        """
        pass

    def get_supported_features(self) -> List[str]:
        """Get list of features supported by this template.

        Returns:
            List of feature names (e.g., ["docker", "github_actions", "rag"])
        """
        return []

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate the provided context for this template.

        Args:
            context: Template context variables

        Returns:
            True if context is valid, False otherwise
        """
        return True

    def pre_generate_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before project generation.

        Args:
            context: Template context variables

        Returns:
            Modified context variables
        """
        return context

    def post_generate_hook(self, project_path: Path, context: Dict[str, Any]) -> None:
        """Hook called after project generation.

        Args:
            project_path: Path to the generated project
            context: Template context variables used during generation
        """
        pass

    def __repr__(self) -> str:
        return f"TemplatePlugin(name='{self.name}', version='{self.version}')"
