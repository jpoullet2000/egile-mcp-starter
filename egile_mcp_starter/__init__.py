"""Egile MCP Starter - A cookiecutter template for MCP servers using FASTMCP
with plugin support."""

__version__ = "1.0.0"
__author__ = "Jean-Baptiste Poullet"
__email__ = "jpoullet2000@gmail.com"

from .cli import main
from .generator import MCPProjectGenerator
from .plugins.base import TemplatePlugin
from .plugins.registry import get_registry

__all__ = ["MCPProjectGenerator", "main", "get_registry", "TemplatePlugin"]
