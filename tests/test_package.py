"""Tests for the main package."""

from egile_mcp_starter import __version__, __author__, __email__


def test_package_metadata():
    """Test that package metadata is correctly defined."""
    assert __version__ == "1.0.0"
    assert __author__ == "Jean-Baptiste Poullet"
    assert __email__ == "jpoullet2000@gmail.com"


def test_package_imports():
    """Test that main package components can be imported."""
    from egile_mcp_starter import MCPProjectGenerator, main

    assert MCPProjectGenerator is not None
    assert main is not None
