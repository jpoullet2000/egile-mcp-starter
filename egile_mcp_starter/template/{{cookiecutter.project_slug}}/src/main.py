#!/usr/bin/env python3
"""
{{ cookiecutter.project_name }} - MCP Server

{{ cookiecutter.project_description }}

This is the main entry point for the MCP server.
"""

import asyncio
import logging
import sys
from pathlib import Path

import click
from fastmcp import FastMCP

# Add the source directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from {{ cookiecutter.project_slug }}.server import create_server
from {{ cookiecutter.project_slug }}.config import load_config, MCPConfig


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file",
)
@click.option(
    "--host",
    default="localhost",
    help="Host to bind the server to",
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port to bind the server to",
)
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="Logging level",
)
def main(
    config: Path | None = None,
    host: str = "localhost",
    port: int = 8000,
    log_level: str = "INFO",
) -> None:
    """Run the {{ cookiecutter.project_name }} MCP server."""
    
    # Setup logging
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting {{ cookiecutter.project_name }} MCP Server")
    
    try:
        # Load configuration
        if config:
            mcp_config = load_config(config)
            logger.info(f"Loaded configuration from {config}")
        else:
            mcp_config = MCPConfig()
            logger.info("Using default configuration")
        
        # Override config with CLI arguments
        mcp_config.host = host
        mcp_config.port = port
        mcp_config.log_level = log_level
        
        # Create and run the server
        server = create_server(mcp_config)
        
        logger.info(f"Server starting on {host}:{port}")
        logger.info("Press Ctrl+C to stop the server")
        
        # Run the server
        asyncio.run(server.run())
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
