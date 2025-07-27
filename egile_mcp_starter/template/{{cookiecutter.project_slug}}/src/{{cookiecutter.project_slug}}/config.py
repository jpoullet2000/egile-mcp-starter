"""Configuration management for {{ cookiecutter.project_name }}."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class MCPConfig(BaseModel):
    """Configuration model for the MCP server."""
    
    # Server settings
    host: str = Field(default="localhost", description="Host to bind the server to")
    port: int = Field(default=8000, description="Port to bind the server to")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # MCP specific settings
    server_name: str = Field(default="{{ cookiecutter.project_name }}", description="MCP server name")
    server_version: str = Field(default="{{ cookiecutter.version }}", description="MCP server version")
    
    # Feature flags
    {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
    enable_tools: bool = Field(default=True, description="Enable tool support")
    {% else -%}
    enable_tools: bool = Field(default=False, description="Enable tool support")
    {% endif -%}
    {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
    enable_resources: bool = Field(default=True, description="Enable resource support")
    {% else -%}
    enable_resources: bool = Field(default=False, description="Enable resource support")
    {% endif -%}
    {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
    enable_prompts: bool = Field(default=True, description="Enable prompt support")
    {% else -%}
    enable_prompts: bool = Field(default=False, description="Enable prompt support")
    {% endif %}
    
    # Custom settings - add your own configuration options here
    custom_settings: Dict[str, Any] = Field(default_factory=dict, description="Custom configuration settings")
    
    class Config:
        """Pydantic configuration."""
        env_prefix = "MCP_"
        case_sensitive = False
        
    @classmethod
    def from_env(cls) -> "MCPConfig":
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv("MCP_HOST", "localhost"),
            port=int(os.getenv("MCP_PORT", "8000")),
            log_level=os.getenv("MCP_LOG_LEVEL", "INFO"),
            server_name=os.getenv("MCP_SERVER_NAME", "{{ cookiecutter.project_name }}"),
            server_version=os.getenv("MCP_SERVER_VERSION", "{{ cookiecutter.version }}"),
            {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
            enable_tools=os.getenv("MCP_ENABLE_TOOLS", "true").lower() == "true",
            {% else -%}
            enable_tools=os.getenv("MCP_ENABLE_TOOLS", "false").lower() == "true",
            {% endif -%}
            {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
            enable_resources=os.getenv("MCP_ENABLE_RESOURCES", "true").lower() == "true",
            {% else -%}
            enable_resources=os.getenv("MCP_ENABLE_RESOURCES", "false").lower() == "true",
            {% endif -%}
            {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
            enable_prompts=os.getenv("MCP_ENABLE_PROMPTS", "true").lower() == "true",
            {% else -%}
            enable_prompts=os.getenv("MCP_ENABLE_PROMPTS", "false").lower() == "true",
            {% endif %}
        )


def load_config(config_file: Path) -> MCPConfig:
    """Load configuration from a YAML file.
    
    Args:
        config_file: Path to the configuration file
        
    Returns:
        MCPConfig instance
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the config file is invalid YAML
        ValueError: If the configuration is invalid
    """
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        if config_data is None:
            config_data = {}
            
        return MCPConfig(**config_data)
        
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}") from e
    except Exception as e:
        raise ValueError(f"Invalid configuration: {e}") from e


def save_config(config: MCPConfig, config_file: Path) -> None:
    """Save configuration to a YAML file.
    
    Args:
        config: MCPConfig instance to save
        config_file: Path where to save the configuration
    """
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config.dict(), f, default_flow_style=False, indent=2)


def get_default_config_path() -> Path:
    """Get the default configuration file path.
    
    Returns:
        Path to the default configuration file
    """
    return Path.home() / ".config" / "{{ cookiecutter.project_slug }}" / "config.yaml"
