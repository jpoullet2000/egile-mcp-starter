"""Main entry point for the RAG MCP server."""

import asyncio
import os
from pathlib import Path

from .server import create_rag_server


async def main():
    """Run the RAG MCP server."""
    # Get configuration path from environment or use default
    config_path = os.getenv("CONFIG_PATH", "config.yaml")

    if not Path(config_path).exists():
        print(f"Configuration file not found: {config_path}")
        print("Please copy config.example.yaml to config.yaml and configure it.")
        return

    # Create and run the server
    server = create_rag_server(config_path)

    # Run the server
    async with server:
        await server.run()


if __name__ == "__main__":
    asyncio.run(main())
