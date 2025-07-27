"""Test configuration for the egile-mcp-starter package."""

import pytest
from pathlib import Path


@pytest.fixture
def template_dir():
    """Get the template directory path."""
    return Path(__file__).parent.parent / "egile_mcp_starter" / "template"


@pytest.fixture
def sample_cookiecutter_json():
    """Sample cookiecutter.json content for testing."""
    return {
        "project_name": "Test MCP Server",
        "project_slug": "test_mcp_server",
        "project_description": "A test MCP server",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "version": "0.1.0",
        "python_version": "3.11",
        "use_docker": "y",
        "use_github_actions": "y",
        "use_pre_commit": "y",
        "license": "MIT",
        "include_examples": "y",
        "server_type": "full",
    }
