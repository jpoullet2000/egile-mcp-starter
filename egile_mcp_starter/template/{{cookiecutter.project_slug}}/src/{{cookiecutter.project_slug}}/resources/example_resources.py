"""Example resources for {{ cookiecutter.project_name }}.

This module contains example resource implementations to demonstrate how to create
MCP resources using the FASTMCP framework.

{% if cookiecutter.include_examples == "y" -%}
These examples are included in your project to help you get started.
{% else -%}
Example resources are not included in this configuration.
{% endif %}
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict
from fastmcp import FastMCP

logger = logging.getLogger(__name__)


def register_example_resources(server: FastMCP) -> None:
    """Register example resources with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    
    @server.resource("file://config")
    async def config_resource() -> str:
        """Provide access to server configuration.
        
        Returns:
            JSON string containing server configuration
        """
        logger.info("Config resource accessed")
        
        config_data = {
            "server_name": "{{ cookiecutter.project_name }}",
            "version": "{{ cookiecutter.version }}",
            "description": "{{ cookiecutter.project_description }}",
            "capabilities": {
                {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
                "tools": True,
                {% else -%}
                "tools": False,
                {% endif -%}
                {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
                "resources": True,
                {% else -%}
                "resources": False,
                {% endif -%}
                {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
                "prompts": True,
                {% else -%}
                "prompts": False,
                {% endif %}
            },
            "runtime": {
                "python_version": "{{ cookiecutter.python_version }}",
                "framework": "FASTMCP"
            }
        }
        
        return json.dumps(config_data, indent=2)
    
    @server.resource("file://logs")
    async def logs_resource() -> str:
        """Provide access to recent server logs.
        
        Returns:
            Text string containing recent log entries
        """
        logger.info("Logs resource accessed")
        
        # In a real implementation, you would read from actual log files
        # This is just a mock implementation
        log_entries = [
            f"{datetime.now().isoformat()} - INFO - Server started",
            f"{datetime.now().isoformat()} - INFO - Resources registered",
            f"{datetime.now().isoformat()} - INFO - Server ready to accept connections",
            f"{datetime.now().isoformat()} - INFO - Logs resource accessed"
        ]
        
        return "\n".join(log_entries)
    
    @server.resource("file://status")
    async def status_resource() -> str:
        """Provide server status and health information.
        
        Returns:
            JSON string containing server status
        """
        logger.info("Status resource accessed")
        
        status_data = {
            "status": "healthy",
            "uptime": "N/A",  # In a real implementation, calculate actual uptime
            "last_check": datetime.now().isoformat(),
            "memory_usage": "N/A",  # In a real implementation, get actual memory usage
            "active_connections": 0,
            "requests_processed": 0,
            "health_checks": {
                "database": "N/A",
                "external_apis": "N/A",
                "disk_space": "OK"
            }
        }
        
        return json.dumps(status_data, indent=2)
    
    @server.resource("file://system-info")
    async def system_info_resource() -> str:
        """Provide system information.
        
        Returns:
            JSON string containing system information
        """
        import platform
        import sys
        
        logger.info("System info resource accessed")
        
        system_data = {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            },
            "python": {
                "version": sys.version,
                "executable": sys.executable,
                "platform": sys.platform
            },
            "server": {
                "name": "{{ cookiecutter.project_name }}",
                "version": "{{ cookiecutter.version }}",
                "framework": "FASTMCP"
            }
        }
        
        return json.dumps(system_data, indent=2)
    
    logger.info("Example resources registered successfully")
