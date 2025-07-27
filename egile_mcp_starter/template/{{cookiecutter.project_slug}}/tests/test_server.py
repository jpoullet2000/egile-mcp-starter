"""Tests for the main server functionality."""

import pytest
from unittest.mock import patch, MagicMock
from {{ cookiecutter.project_slug }}.server import create_server, get_server_info, setup_server_middleware
from {{ cookiecutter.project_slug }}.config import MCPConfig


class TestServerCreation:
    """Test server creation and configuration."""
    
    def test_create_server_with_default_config(self, test_config: MCPConfig):
        """Test creating a server with default configuration."""
        server = create_server(test_config)
        
        assert server is not None
        assert server.host == test_config.host
        assert server.port == test_config.port
    
    def test_create_server_with_custom_config(self):
        """Test creating a server with custom configuration."""
        config = MCPConfig(
            host="custom-host",
            port=9999,
            server_name="Custom Server",
            server_version="2.0.0",
        )
        
        server = create_server(config)
        
        assert server is not None
        assert server.host == "custom-host"
        assert server.port == 9999
    
    {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
    def test_server_with_tools_enabled(self):
        """Test server creation with tools enabled."""
        config = MCPConfig(enable_tools=True)
        server = create_server(config)
        
        assert server is not None
        # Add specific tool-related assertions here
    
    def test_server_with_tools_disabled(self):
        """Test server creation with tools disabled."""
        config = MCPConfig(enable_tools=False)
        server = create_server(config)
        
        assert server is not None
        # Add specific assertions for disabled tools here
    
    {% endif -%}
    {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
    def test_server_with_resources_enabled(self):
        """Test server creation with resources enabled."""
        config = MCPConfig(enable_resources=True)
        server = create_server(config)
        
        assert server is not None
        # Add specific resource-related assertions here
    
    def test_server_with_resources_disabled(self):
        """Test server creation with resources disabled."""
        config = MCPConfig(enable_resources=False)
        server = create_server(config)
        
        assert server is not None
        # Add specific assertions for disabled resources here
    
    {% endif -%}
    {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
    def test_server_with_prompts_enabled(self):
        """Test server creation with prompts enabled."""
        config = MCPConfig(enable_prompts=True)
        server = create_server(config)
        
        assert server is not None
        # Add specific prompt-related assertions here
    
    def test_server_with_prompts_disabled(self):
        """Test server creation with prompts disabled."""
        config = MCPConfig(enable_prompts=False)
        server = create_server(config)
        
        assert server is not None
        # Add specific assertions for disabled prompts here
    
    {% endif %}

class TestServerInfo:
    """Test server information functionality."""
    
    def test_get_server_info(self, test_config: MCPConfig):
        """Test getting server information."""
        info = get_server_info(test_config)
        
        assert isinstance(info, dict)
        assert info["name"] == test_config.server_name
        assert info["version"] == test_config.server_version
        assert info["host"] == test_config.host
        assert info["port"] == test_config.port
        assert info["log_level"] == test_config.log_level
        assert "capabilities" in info
        assert "description" in info
    
    def test_server_info_capabilities(self, test_config: MCPConfig):
        """Test server capabilities in info."""
        info = get_server_info(test_config)
        capabilities = info["capabilities"]
        
        {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
        assert "tools" in capabilities
        assert capabilities["tools"] == test_config.enable_tools
        {% endif -%}
        {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
        assert "resources" in capabilities
        assert capabilities["resources"] == test_config.enable_resources
        {% endif -%}
        {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
        assert "prompts" in capabilities
        assert capabilities["prompts"] == test_config.enable_prompts
        {% endif %}


class TestServerMiddleware:
    """Test server middleware and hooks."""
    
    @pytest.mark.asyncio
    async def test_setup_server_middleware(self, test_server):
        """Test setting up server middleware."""
        # This test would need to be adapted based on the actual FASTMCP API
        # For now, just test that the function runs without error
        setup_server_middleware(test_server, MCPConfig())
    
    @patch('{{ cookiecutter.project_slug }}.server.logger')
    def test_middleware_logging(self, mock_logger, test_server):
        """Test that middleware setup logs appropriately."""
        config = MCPConfig()
        setup_server_middleware(test_server, config)
        
        # Verify that the middleware setup doesn't raise exceptions
        # In a real implementation, you might check for specific log messages


class TestServerIntegration:
    """Integration tests for the server."""
    
    def test_full_server_setup(self):
        """Test complete server setup with all features."""
        config = MCPConfig(
            host="localhost",
            port=8080,
            server_name="Integration Test Server",
            {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
            enable_tools=True,
            {% endif -%}
            {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
            enable_resources=True,
            {% endif -%}
            {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
            enable_prompts=True,
            {% endif %}
        )
        
        server = create_server(config)
        setup_server_middleware(server, config)
        
        assert server is not None
        
        # Test server info
        info = get_server_info(config)
        assert info["name"] == "Integration Test Server"
        
    def test_minimal_server_setup(self):
        """Test minimal server setup with no optional features."""
        config = MCPConfig(
            host="localhost",
            port=8081,
            enable_tools=False,
            enable_resources=False,
            enable_prompts=False,
        )
        
        server = create_server(config)
        
        assert server is not None
        assert server.host == "localhost"
        assert server.port == 8081
