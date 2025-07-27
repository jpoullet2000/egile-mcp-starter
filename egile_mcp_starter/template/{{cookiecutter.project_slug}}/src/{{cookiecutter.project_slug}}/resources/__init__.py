"""Resource implementations for {{ cookiecutter.project_name }}.

This module contains the MCP resource implementations that provide access to data
and information that AI systems can use.

{% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
This server includes resource support.
{% else -%}
Resource support is disabled for this server type.
{% endif %}
"""

from typing import Any, Dict, List
from fastmcp import FastMCP
import logging

{% if cookiecutter.include_examples == "y" -%}
from .example_resources import register_example_resources

{% endif %}

logger = logging.getLogger(__name__)


def register_resources(server: FastMCP) -> None:
    """Register all resources with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
    logger.info("Registering MCP resources...")
    
    {% if cookiecutter.include_examples == "y" -%}
    # Register example resources
    register_example_resources(server)
    
    {% endif %}
    # Register your custom resources here
    # Example:
    # register_custom_resources(server)
    
    logger.info("All resources registered successfully")
    {% else -%}
    logger.warning("Resource support is disabled - no resources will be registered")
    {% endif %}


def get_available_resources() -> List[Dict[str, Any]]:
    """Get a list of all available resources.
    
    Returns:
        List of resource definitions
    """
    {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
    resources = []
    
    {% if cookiecutter.include_examples == "y" -%}
    # Add example resources to the list
    resources.extend([
        {
            "uri": "file://config",
            "name": "Server Configuration",
            "description": "Current server configuration settings",
            "mimeType": "application/json"
        },
        {
            "uri": "file://logs",
            "name": "Server Logs",
            "description": "Recent server log entries",
            "mimeType": "text/plain"
        },
        {
            "uri": "file://status",
            "name": "Server Status",
            "description": "Current server status and health information",
            "mimeType": "application/json"
        }
    ])
    
    {% endif %}
    # Add your custom resources to the list here
    
    return resources
    {% else -%}
    return []
    {% endif %}
