"""Prompt implementations for {{ cookiecutter.project_name }}.

This module contains the MCP prompt implementations that provide prompt templates
that AI systems can use for various tasks.

{% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
This server includes prompt support.
{% else -%}
Prompt support is disabled for this server type.
{% endif %}
"""

from typing import Any, Dict, List
from fastmcp import FastMCP
import logging

{% if cookiecutter.include_examples == "y" -%}
from .example_prompts import register_example_prompts

{% endif %}

logger = logging.getLogger(__name__)


def register_prompts(server: FastMCP) -> None:
    """Register all prompts with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
    logger.info("Registering MCP prompts...")
    
    {% if cookiecutter.include_examples == "y" -%}
    # Register example prompts
    register_example_prompts(server)
    
    {% endif %}
    # Register your custom prompts here
    # Example:
    # register_custom_prompts(server)
    
    logger.info("All prompts registered successfully")
    {% else -%}
    logger.warning("Prompt support is disabled - no prompts will be registered")
    {% endif %}


def get_available_prompts() -> List[Dict[str, Any]]:
    """Get a list of all available prompts.
    
    Returns:
        List of prompt definitions
    """
    {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
    prompts = []
    
    {% if cookiecutter.include_examples == "y" -%}
    # Add example prompts to the list
    prompts.extend([
        {
            "name": "code_review",
            "description": "A prompt template for conducting code reviews",
            "arguments": [
                {
                    "name": "code",
                    "description": "The code to review",
                    "required": True
                },
                {
                    "name": "language",
                    "description": "Programming language of the code",
                    "required": False
                }
            ]
        },
        {
            "name": "explain_code",
            "description": "A prompt template for explaining code functionality",
            "arguments": [
                {
                    "name": "code",
                    "description": "The code to explain",
                    "required": True
                },
                {
                    "name": "detail_level",
                    "description": "Level of detail for the explanation (basic, detailed, expert)",
                    "required": False
                }
            ]
        },
        {
            "name": "debug_help",
            "description": "A prompt template for debugging assistance",
            "arguments": [
                {
                    "name": "error_message",
                    "description": "The error message or issue description",
                    "required": True
                },
                {
                    "name": "code_context",
                    "description": "Relevant code context where the error occurs",
                    "required": False
                }
            ]
        }
    ])
    
    {% endif %}
    # Add your custom prompts to the list here
    
    return prompts
    {% else -%}
    return []
    {% endif %}
