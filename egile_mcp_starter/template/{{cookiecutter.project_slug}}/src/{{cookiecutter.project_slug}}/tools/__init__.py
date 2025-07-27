"""Tool implementations for {{ cookiecutter.project_name }}.

This module contains the MCP tool implementations that can be called by AI systems.
Tools provide specific functionality that AI can use to perform tasks.

{% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
This server includes tool support.
{% else -%}
Tool support is disabled for this server type.
{% endif %}
"""

from typing import Any, Dict, List
from fastmcp import FastMCP
import logging

{% if cookiecutter.include_examples == "y" -%}
from .example_tools import register_example_tools

{% endif %}

logger = logging.getLogger(__name__)


def register_tools(server: FastMCP) -> None:
    """Register all tools with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
    logger.info("Registering MCP tools...")
    
    {% if cookiecutter.include_examples == "y" -%}
    # Register example tools
    register_example_tools(server)
    
    {% endif %}
    # Register your custom tools here
    # Example:
    # register_custom_tools(server)
    
    logger.info("All tools registered successfully")
    {% else -%}
    logger.warning("Tool support is disabled - no tools will be registered")
    {% endif %}


def get_available_tools() -> List[Dict[str, Any]]:
    """Get a list of all available tools.
    
    Returns:
        List of tool definitions
    """
    {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
    tools = []
    
    {% if cookiecutter.include_examples == "y" -%}
    # Add example tools to the list
    tools.extend([
        {
            "name": "echo",
            "description": "Echo back the provided text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to echo back"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "calculate",
            "description": "Perform basic mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')"
                    }
                },
                "required": ["expression"]
            }
        }
    ])
    
    {% endif %}
    # Add your custom tools to the list here
    
    return tools
    {% else -%}
    return []
    {% endif %}
