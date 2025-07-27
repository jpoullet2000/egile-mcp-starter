"""Tests for configuration management."""

import pytest
import os
import yaml
from pathlib import Path
from unittest.mock import patch
from {{ cookiecutter.project_slug }}.config import (
    MCPConfig,
    load_config,
    save_config,
    get_default_config_path,
)


class TestMCPConfig:
    """Test MCPConfig model functionality."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = MCPConfig()
        
        assert config.host == "localhost"
        assert config.port == 8000
        assert config.log_level == "INFO"
        assert config.server_name == "{{ cookiecutter.project_name }}"
        assert config.server_version == "{{ cookiecutter.version }}"
        {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
        assert config.enable_tools is True
        {% else -%}
        assert config.enable_tools is False
        {% endif -%}
        {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
        assert config.enable_resources is True
        {% else -%}
        assert config.enable_resources is False
        {% endif -%}
        {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
        assert config.enable_prompts is True
        {% else -%}
        assert config.enable_prompts is False
        {% endif %}
        assert isinstance(config.custom_settings, dict)
    
    def test_custom_config_values(self):
        """Test custom configuration values."""
        config = MCPConfig(
            host="custom-host",
            port=9999,
            log_level="DEBUG",
            server_name="Custom Server",
            server_version="2.0.0",
            enable_tools=False,
            enable_resources=False,
            enable_prompts=False,
            custom_settings={"test": "value"}
        )
        
        assert config.host == "custom-host"
        assert config.port == 9999
        assert config.log_level == "DEBUG"
        assert config.server_name == "Custom Server"
        assert config.server_version == "2.0.0"
        assert config.enable_tools is False
        assert config.enable_resources is False
        assert config.enable_prompts is False
        assert config.custom_settings == {"test": "value"}
    
    def test_config_from_env(self, mock_environment):
        """Test creating configuration from environment variables."""
        config = MCPConfig.from_env()
        
        assert config.host == "test-host"
        assert config.port == 8080
        assert config.log_level == "ERROR"
        assert config.server_name == "Mock Server"
        assert config.server_version == "2.0.0"
        assert config.enable_tools is True
        assert config.enable_resources is False
        assert config.enable_prompts is True


class TestConfigFile:
    """Test configuration file operations."""
    
    def test_load_config_from_file(self, temp_config_file: Path):
        """Test loading configuration from YAML file."""
        config = load_config(temp_config_file)
        
        assert config.host == "0.0.0.0"
        assert config.port == 9000
        assert config.log_level == "WARNING"
        assert config.server_name == "Test Server"
        assert config.server_version == "1.0.0"
        assert config.enable_tools is True
        assert config.enable_resources is True
        assert config.enable_prompts is True
        assert config.custom_settings["test_mode"] is True
        assert config.custom_settings["debug_enabled"] is False
    
    def test_load_config_nonexistent_file(self, tmp_path: Path):
        """Test loading configuration from nonexistent file."""
        nonexistent_file = tmp_path / "nonexistent.yaml"
        
        with pytest.raises(FileNotFoundError):
            load_config(nonexistent_file)
    
    def test_load_config_invalid_yaml(self, tmp_path: Path):
        """Test loading configuration from invalid YAML file."""
        invalid_file = tmp_path / "invalid.yaml"
        invalid_file.write_text("invalid: yaml: content: [")
        
        with pytest.raises(yaml.YAMLError):
            load_config(invalid_file)
    
    def test_load_config_empty_file(self, tmp_path: Path):
        """Test loading configuration from empty file."""
        empty_file = tmp_path / "empty.yaml"
        empty_file.write_text("")
        
        config = load_config(empty_file)
        
        # Should create a default config
        assert config.host == "localhost"
        assert config.port == 8000
    
    def test_save_config(self, tmp_path: Path):
        """Test saving configuration to file."""
        config = MCPConfig(
            host="save-test",
            port=7777,
            log_level="WARNING",
            custom_settings={"saved": True}
        )
        
        config_file = tmp_path / "saved_config.yaml"
        save_config(config, config_file)
        
        assert config_file.exists()
        
        # Load it back and verify
        loaded_config = load_config(config_file)
        assert loaded_config.host == "save-test"
        assert loaded_config.port == 7777
        assert loaded_config.log_level == "WARNING"
        assert loaded_config.custom_settings["saved"] is True
    
    def test_save_config_creates_directory(self, tmp_path: Path):
        """Test that save_config creates directories if they don't exist."""
        config = MCPConfig()
        config_file = tmp_path / "nested" / "directory" / "config.yaml"
        
        save_config(config, config_file)
        
        assert config_file.exists()
        assert config_file.parent.exists()
    
    def test_get_default_config_path(self):
        """Test getting default configuration path."""
        path = get_default_config_path()
        
        assert isinstance(path, Path)
        assert str(path).endswith("{{ cookiecutter.project_slug }}/config.yaml")
        assert ".config" in str(path)


class TestConfigValidation:
    """Test configuration validation and error handling."""
    
    def test_invalid_port_type(self):
        """Test validation with invalid port type."""
        with pytest.raises(ValueError):
            MCPConfig(port="invalid")
    
    def test_invalid_boolean_type(self):
        """Test validation with invalid boolean type."""
        with pytest.raises(ValueError):
            MCPConfig(enable_tools="not a boolean")
    
    def test_config_serialization(self):
        """Test that configuration can be serialized/deserialized."""
        original_config = MCPConfig(
            host="serialize-test",
            port=6666,
            custom_settings={"nested": {"value": 42}}
        )
        
        # Convert to dict and back
        config_dict = original_config.dict()
        new_config = MCPConfig(**config_dict)
        
        assert new_config.host == original_config.host
        assert new_config.port == original_config.port
        assert new_config.custom_settings == original_config.custom_settings


class TestConfigIntegration:
    """Integration tests for configuration."""
    
    @patch.dict(os.environ, {
        "MCP_HOST": "integration-host",
        "MCP_PORT": "5555",
        "MCP_LOG_LEVEL": "DEBUG"
    })
    def test_env_override_integration(self):
        """Test that environment variables properly override defaults."""
        config = MCPConfig.from_env()
        
        assert config.host == "integration-host"
        assert config.port == 5555
        assert config.log_level == "DEBUG"
    
    def test_file_and_env_integration(self, tmp_path: Path):
        """Test combination of file config and environment variables."""
        # Create a config file
        file_config = {
            "host": "file-host",
            "port": 4444,
            "server_name": "File Server"
        }
        
        config_file = tmp_path / "integration.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(file_config, f)
        
        # Load from file
        config = load_config(config_file)
        
        assert config.host == "file-host"
        assert config.port == 4444
        assert config.server_name == "File Server"
