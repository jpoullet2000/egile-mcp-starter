"""Main MCP server implementation using FASTMCP framework."""

import logging
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP
from .config import MCPConfig

{% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
from .tools import register_tools

{% endif -%}
{% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
from .resources import register_resources

{% endif -%}
{% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
from .prompts import register_prompts

{% endif %}

logger = logging.getLogger(__name__)


def create_server(config: MCPConfig) -> FastMCP:
    """Create and configure the MCP server.
    
    Args:
        config: MCP server configuration
        
    Returns:
        Configured FastMCP server instance
    """
    logger.info(f"Creating MCP server: {config.server_name} v{config.server_version}")
    
    # Create FastMCP server instance
    server = FastMCP(
        name=config.server_name,
        version=config.server_version,
    )
    
    # Register capabilities based on configuration
    {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
    if config.enable_tools:
        logger.info("Registering tools...")
        register_tools(server)
        logger.info("Tools registered successfully")
    
    {% endif -%}
    {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
    if config.enable_resources:
        logger.info("Registering resources...")
        register_resources(server)
        logger.info("Resources registered successfully")
    
    {% endif -%}
    {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
    if config.enable_prompts:
        logger.info("Registering prompts...")
        register_prompts(server)
        logger.info("Prompts registered successfully")
    
    {% endif %}
    # Add custom server configuration
    server.host = config.host
    server.port = config.port
    
    logger.info(f"MCP server created and configured on {config.host}:{config.port}")
    
    return server


def setup_server_middleware(server: FastMCP, config: MCPConfig) -> None:
    """Setup server middleware and hooks.
    
    Args:
        server: FastMCP server instance
        config: MCP server configuration
    """
    
    @server.on_startup
    async def startup_handler():
        """Handle server startup."""
        logger.info("{{ cookiecutter.project_name }} MCP server starting up...")
        
        # Add any startup logic here
        # Example: Initialize databases, load models, etc.
        
        logger.info("Startup complete")
    
    @server.on_shutdown
    async def shutdown_handler():
        """Handle server shutdown."""
        logger.info("{{ cookiecutter.project_name }} MCP server shutting down...")
        
        # Add any cleanup logic here
        # Example: Close database connections, save state, etc.
        
        logger.info("Shutdown complete")
    
    @server.on_error
    async def error_handler(error: Exception):
        """Handle server errors."""
        logger.error(f"Server error: {error}")
        
        # Add custom error handling logic here
        # Example: Send alerts, log to external services, etc.


def get_server_info(config: MCPConfig) -> Dict[str, Any]:
    """Get server information and capabilities.
    
    Args:
        config: MCP server configuration
        
    Returns:
        Dictionary containing server information
    """
    return {
        "name": config.server_name,
        "version": config.server_version,
        "description": "{{ cookiecutter.project_description }}",
        "capabilities": {
            {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
            "tools": config.enable_tools,
            {% endif -%}
            {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
            "resources": config.enable_resources,
            {% endif -%}
            {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
            "prompts": config.enable_prompts,
            {% endif %}
        },
        "host": config.host,
        "port": config.port,
        "log_level": config.log_level,
    }
