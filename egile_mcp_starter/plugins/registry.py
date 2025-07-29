"""Template registry for managing template plugins."""

import importlib.util
from pathlib import Path
from typing import Dict, List, Optional

from .base import TemplatePlugin


class TemplateRegistry:
    """Registry for managing template plugins."""

    def __init__(self) -> None:
        """Initialize the template registry."""
        self._plugins: Dict[str, TemplatePlugin] = {}
        self._discover_builtin_templates()

    def register(self, plugin: TemplatePlugin) -> None:
        """Register a template plugin.

        Args:
            plugin: Template plugin to register

        Raises:
            ValueError: If a plugin with the same name is already registered
        """
        if plugin.name in self._plugins:
            raise ValueError(f"Template plugin '{plugin.name}' is already registered")

        self._plugins[plugin.name] = plugin

    def unregister(self, name: str) -> None:
        """Unregister a template plugin.

        Args:
            name: Name of the plugin to unregister
        """
        self._plugins.pop(name, None)

    def get_plugin(self, name: str) -> Optional[TemplatePlugin]:
        """Get a template plugin by name.

        Args:
            name: Name of the template plugin

        Returns:
            Template plugin or None if not found
        """
        return self._plugins.get(name)

    def list_plugins(self) -> List[TemplatePlugin]:
        """List all registered template plugins.

        Returns:
            List of registered template plugins
        """
        return list(self._plugins.values())

    def get_plugin_names(self) -> List[str]:
        """Get names of all registered template plugins.

        Returns:
            List of plugin names
        """
        return list(self._plugins.keys())

    def _discover_builtin_templates(self) -> None:
        """Discover and register built-in template plugins."""
        # Register the default MCP template
        from .builtin.mcp_template import MCPTemplatePlugin

        self.register(MCPTemplatePlugin())

        # Register the RAG template
        from .builtin.rag_template import RAGTemplatePlugin

        self.register(RAGTemplatePlugin())

        # Try to discover additional built-in templates
        builtin_dir = Path(__file__).parent / "builtin"
        if builtin_dir.exists():
            for plugin_file in builtin_dir.glob("*_template.py"):
                if plugin_file.name in ["mcp_template.py", "rag_template.py"]:
                    continue  # Already registered above

                try:
                    self._load_builtin_plugin(plugin_file)
                except Exception:
                    # Silently skip plugins that fail to load
                    pass

    def _load_builtin_plugin(self, plugin_file: Path) -> None:
        """Load a built-in plugin from a file.

        Args:
            plugin_file: Path to the plugin file
        """
        module_name = plugin_file.stem
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)

        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Look for plugin classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, TemplatePlugin)
                    and attr != TemplatePlugin
                ):
                    try:
                        plugin_instance = attr()  # type: ignore[call-arg]
                        self.register(plugin_instance)
                    except Exception:
                        pass  # Skip plugins that fail to instantiate

    def discover_external_plugins(self) -> None:
        """Discover external template plugins via entry points."""
        try:
            try:
                # Python 3.8+
                from importlib.metadata import entry_points
            except ImportError:
                # Python < 3.8
                from importlib_metadata import entry_points  # type: ignore

            for entry_point in entry_points(group="egile_mcp_starter.templates"):
                try:
                    plugin_class = entry_point.load()
                    plugin_instance = plugin_class()
                    self.register(plugin_instance)
                except Exception:
                    pass  # Skip plugins that fail to load
        except ImportError:
            # pkg_resources not available
            pass


# Global registry instance
_registry = TemplateRegistry()


def get_registry() -> TemplateRegistry:
    """Get the global template registry instance.

    Returns:
        Global template registry
    """
    return _registry
