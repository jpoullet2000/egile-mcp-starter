"""Test configuration and fixtures for {{ cookiecutter.project_name }}."""

import pytest
import logging
from pathlib import Path
from typing import Dict, Any
from {{ cookiecutter.project_slug }}.config import MCPConfig
from {{ cookiecutter.project_slug }}.server import create_server


@pytest.fixture
def test_config() -> MCPConfig:
    """Create a test configuration."""
    return MCPConfig(
        host="localhost",
        port=8001,  # Use different port for testing
        log_level="DEBUG",
        server_name="{{ cookiecutter.project_name }} Test",
        server_version="{{ cookiecutter.version }}",
        {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
        enable_tools=True,
        {% else -%}
        enable_tools=False,
        {% endif -%}
        {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
        enable_resources=True,
        {% else -%}
        enable_resources=False,
        {% endif -%}
        {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
        enable_prompts=True,
        {% else -%}
        enable_prompts=False,
        {% endif %}
    )


@pytest.fixture
def test_server(test_config: MCPConfig):
    """Create a test MCP server."""
    return create_server(test_config)


@pytest.fixture
def sample_config_data() -> Dict[str, Any]:
    """Sample configuration data for testing."""
    return {
        "host": "0.0.0.0",
        "port": 9000,
        "log_level": "WARNING",
        "server_name": "Test Server",
        "server_version": "1.0.0",
        "enable_tools": True,
        "enable_resources": True,
        "enable_prompts": True,
        "custom_settings": {
            "test_mode": True,
            "debug_enabled": False
        }
    }


@pytest.fixture
def temp_config_file(tmp_path: Path, sample_config_data: Dict[str, Any]) -> Path:
    """Create a temporary configuration file for testing."""
    import yaml
    
    config_file = tmp_path / "test_config.yaml"
    
    with open(config_file, 'w') as f:
        yaml.dump(sample_config_data, f)
    
    return config_file


@pytest.fixture(autouse=True)
def setup_test_logging():
    """Setup logging for tests."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


@pytest.fixture
def mock_environment(monkeypatch):
    """Mock environment variables for testing."""
    test_env = {
        "MCP_HOST": "test-host",
        "MCP_PORT": "8080",
        "MCP_LOG_LEVEL": "ERROR",
        "MCP_SERVER_NAME": "Mock Server",
        "MCP_SERVER_VERSION": "2.0.0",
        "MCP_ENABLE_TOOLS": "true",
        "MCP_ENABLE_RESOURCES": "false",
        "MCP_ENABLE_PROMPTS": "true",
    }
    
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    
    return test_env
