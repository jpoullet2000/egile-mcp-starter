"""Egile MCP Starter - A cookiecutter template for MCP servers using FASTMCP."""

__version__ = "1.0.0"
__author__ = "Jean-Baptiste Poullet"
__email__ = "jpoullet2000@gmail.com"

from .cli import main
from .generator import MCPProjectGenerator

__all__ = ["MCPProjectGenerator", "main"]
