"""{{ cookiecutter.project_name }} - MCP Server Package

{{ cookiecutter.project_description }}

Built with FASTMCP framework for the Model Context Protocol.
"""

__version__ = "{{ cookiecutter.version }}"
__author__ = "{{ cookiecutter.author_name }}"
__email__ = "{{ cookiecutter.author_email }}"

from .server import create_server
from .config import MCPConfig, load_config

__all__ = ["create_server", "MCPConfig", "load_config"]
