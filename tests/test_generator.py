"""Test the egile-mcp-starter package functionality."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from egile_mcp_starter.generator import MCPProjectGenerator


class TestMCPProjectGenerator:
    """Test the MCP project generator."""

    def test_generator_initialization(self):
        """Test that the generator initializes correctly."""
        generator = MCPProjectGenerator()

        assert generator.output_dir == Path.cwd()
        assert generator.no_input is False
        assert generator.config_file is None
        assert generator.verbose is False
        assert generator.template_dir.exists()

    def test_generator_with_custom_params(self):
        """Test generator with custom parameters."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            generator = MCPProjectGenerator(
                output_dir=tmp_dir, no_input=True, verbose=True
            )

            assert str(generator.output_dir) == tmp_dir
            assert generator.no_input is True
            assert generator.verbose is True

    def test_get_default_context(self):
        """Test getting default context values."""
        generator = MCPProjectGenerator()
        context = generator.get_default_context()

        assert isinstance(context, dict)
        assert "project_name" in context
        assert "project_slug" in context
        assert "author_name" in context
        assert "python_version" in context
        assert context["project_name"] == "my-mcp-server"
        assert context["python_version"] == "3.11"

    @patch("egile_mcp_starter.generator.cookiecutter")
    def test_generate_project_success(self, mock_cookiecutter):
        """Test successful project generation."""
        mock_cookiecutter.return_value = "/tmp/test-project"

        generator = MCPProjectGenerator(no_input=True, verbose=True)
        result = generator.generate()

        assert result == Path("/tmp/test-project")
        mock_cookiecutter.assert_called_once()

    @patch("egile_mcp_starter.generator.cookiecutter")
    def test_generate_project_failure(self, mock_cookiecutter):
        """Test project generation failure handling."""
        mock_cookiecutter.side_effect = Exception("Template error")

        generator = MCPProjectGenerator()

        with pytest.raises(Exception) as exc_info:
            generator.generate()

        assert "Failed to generate MCP server project" in str(exc_info.value)

    def test_generate_without_cookiecutter(self):
        """Test generation when cookiecutter is not available."""
        with patch("egile_mcp_starter.generator.cookiecutter", None):
            generator = MCPProjectGenerator()

            with pytest.raises(Exception) as exc_info:
                generator.generate()

            assert "cookiecutter is not installed" in str(exc_info.value)
