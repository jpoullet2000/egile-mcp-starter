# egile-mcp-starter

[![PyPI - Version](https://img.shields.io/pypi/v/egile-mcp-starter.svg)](https://pypi.org/project/egile-mcp-starter)
[![Tests](https://github.com/jpoullet2000/egile-mcp-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/jpoullet2000/egile-mcp-starter/actions/workflows/ci.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/egile-mcp-starter.svg)](https://pypi.org/project/egile-mcp-starter)
[![License](https://img.shields.io/github/license/jpoullet2000/egile-mcp-starter.svg)](https://github.com/jpoullet2000/egile-mcp-starter/blob/main/LICENSE)
[![Docker](https://img.shields.io/docker/automated/jpoullet2000/egile-mcp-starter.svg)](https://hub.docker.com/r/jpoullet2000/egile-mcp-starter)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![FastMCP](https://img.shields.io/badge/built%20with-FastMCP-green.svg)](https://github.com/jlowin/fastmcp)
[![MCP](https://img.shields.io/badge/protocol-MCP-orange.svg)](https://modelcontextprotocol.io/)

A comprehensive cookiecutter template for creating Model Context Protocol (MCP) servers using the FASTMCP framework.

## Features

- 🚀 **Modern Python Setup**: Uses Poetry for dependency management and packaging
- 🏗️ **FASTMCP Framework**: Built on the efficient FASTMCP framework for MCP servers
- 🛠️ **Flexible Server Types**: Choose from tools, resources, prompts, or full-featured servers
- 🧪 **Testing Ready**: Comprehensive test suite with pytest and coverage
- 🔧 **Development Tools**: Pre-configured with Black, Flake8, MyPy, and pre-commit hooks
- 🐳 **Docker Support**: Optional Docker configuration for easy deployment
- 🔄 **CI/CD Ready**: GitHub Actions workflows for automated testing and deployment
- 📚 **Rich Documentation**: Detailed README and code documentation
- 🎛️ **Configurable**: YAML-based configuration with environment variable support

## Quick Start

### Installation

```bash
# Install with Poetry (recommended)
pip install egile-mcp-starter

# Or install from source
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter
poetry install
```

### Generate a New MCP Server

```bash
# Using the installed command
egile-mcp-starter

# Or if installed from source
poetry run egile-mcp-starter

# With options
egile-mcp-starter --output-dir ./my-projects --verbose
```

### Available Server Types

When generating a project, you can choose from:

- **tools**: Server with tool implementations for AI interactions
- **resources**: Server with resource management for data access  
- **prompts**: Server with prompt templates for AI guidance
- **full**: Complete server with all capabilities (tools, resources, and prompts)

## Generated Project Structure

The generated project will have this structure:

```
my-mcp-server/
├── src/
│   ├── my_mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py          # Main MCP server implementation
│   │   ├── config.py          # Configuration management
│   │   ├── tools/             # Tool implementations (if enabled)
│   │   ├── resources/         # Resource handlers (if enabled)
│   │   ├── prompts/           # Prompt templates (if enabled)
│   │   └── utils.py           # Utility functions
│   └── main.py                # Entry point
├── tests/                     # Comprehensive test suite
├── pyproject.toml            # Poetry configuration
├── README.md                 # Project documentation
├── Dockerfile               # Docker configuration (optional)
└── .github/workflows/       # CI/CD workflows (optional)
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter

# Install dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=egile_mcp_starter --cov-report=html

# Run specific tests
poetry run pytest tests/test_generator.py -v
```

### Code Quality

```bash
# Format code
poetry run black .

# Check linting
poetry run flake8 egile_mcp_starter tests

# Type checking
poetry run mypy egile_mcp_starter

# Run all pre-commit checks
poetry run pre-commit run --all-files
```

## Configuration Options

The cookiecutter template supports these configuration options:

| Option | Description | Choices |
|--------|-------------|---------|
| `project_name` | Display name for your project | String |
| `project_slug` | Python package name | Auto-generated |
| `project_description` | Project description | String |
| `author_name` | Your name | String |
| `author_email` | Your email | String |
| `github_username` | Your GitHub username | String |
| `version` | Initial version | String (default: 0.1.0) |
| `python_version` | Python version | 3.8, 3.9, 3.10, 3.11, 3.12 |
| `use_docker` | Include Docker support | y/n |
| `use_github_actions` | Include CI/CD workflows | y/n |
| `use_pre_commit` | Include pre-commit hooks | y/n |
| `license` | Project license | MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, None |
| `include_examples` | Include example implementations | y/n |
| `server_type` | Type of MCP server | tools, resources, prompts, full |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`poetry run pytest`)
5. Run code quality checks (`poetry run pre-commit run --all-files`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: jpoullet2000@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/jpoullet2000/egile-mcp-starter/issues)
- 📖 MCP Documentation: [Model Context Protocol](https://modelcontextprotocol.io/)
- 🚀 FASTMCP: [FASTMCP Framework](https://github.com/jlowin/fastmcp)

---

Built with ❤️ using [FASTMCP](https://github.com/jlowin/fastmcp) and the [Model Context Protocol](https://modelcontextprotocol.io/)

## Overview

The Model Context Protocol (MCP) is a standardized protocol for communication between AI systems and external tools/data sources. This template provides a complete foundation for building MCP servers with:

- 🛠️ **Tool Support** - Implement custom tools that AI can call
- 📚 **Resource Support** - Provide data and information access
- 💬 **Prompt Support** - Create reusable prompt templates
- 🧪 **Testing Framework** - Comprehensive test coverage
- 🔧 **Development Tools** - Linting, formatting, type checking
- 🐳 **Docker Support** - Container deployment ready
- 🔄 **CI/CD Pipeline** - GitHub Actions integration
- 📋 **Type Safety** - Full type annotations throughout

## Features

### 🎯 **Template Options**

- **Server Types**: Choose from tools, resources, prompts, or full MCP server
- **Python Versions**: Support for Python 3.8-3.12
- **Docker Integration**: Optional Docker and docker-compose setup
- **CI/CD Ready**: GitHub Actions workflow included
- **Development Tools**: Pre-commit hooks, linting, testing
- **Documentation**: Auto-generated README and examples

### 🛠️ **Built-in Capabilities**

- **Configuration Management**: YAML-based config with environment variable override
- **Logging**: Structured logging with configurable levels
- **Error Handling**: Comprehensive error handling and validation
- **Type Safety**: Full type annotations with mypy checking
- **Testing**: pytest-based testing with coverage reporting
- **Security**: Built-in security scanning and best practices

## Quick Start

### Installation

```bash
# Install the package
pip install egile-mcp-starter

# Or install from source
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter
pip install -e .
```

### Generate a New MCP Server

```bash
# Use the CLI tool
egile-mcp-starter

# Or use cookiecutter directly
cookiecutter https://github.com/jpoullet2000/egile-mcp-starter.git
```

### Interactive Configuration

The template will prompt you for:

- **Project name and description**
- **Author information**
- **Server type** (tools, resources, prompts, or full)
- **Python version** (3.8-3.12)
- **Optional features** (Docker, GitHub Actions, pre-commit)
- **License choice** (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, or None)

### Example Usage

```bash
$ egile-mcp-starter
project_name [My MCP Server]: Weather MCP Server
project_description [A Model Context Protocol server built with FASTMCP]: Weather data MCP server with forecast tools
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
server_type [full]: tools
python_version [3.11]: 3.11
use_docker [y]: y
use_github_actions [y]: y
include_examples [y]: y

✅ MCP server project generated successfully at: ./weather_mcp_server
```

## Generated Project Structure

```
my_mcp_server/
├── src/
│   ├── my_mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py          # Main MCP server
│   │   ├── config.py          # Configuration management
│   │   ├── tools/             # Tool implementations
│   │   ├── resources/         # Resource handlers
│   │   ├── prompts/           # Prompt templates
│   │   └── utils.py           # Utility functions
│   └── main.py                # Entry point
├── tests/                     # Test suite
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── .github/workflows/ci.yml   # GitHub Actions CI/CD
├── .pre-commit-config.yaml    # Pre-commit hooks
├── pyproject.toml             # Project configuration
├── poetry.lock                # Locked dependencies
└── README.md                  # Project documentation
```

## Development Workflow

### 1. Generate Your Project

```bash
egile-mcp-starter
cd your-project-name
```

### 2. Set Up Development Environment

```bash
# Install dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks (if enabled)
pre-commit install
```

### 3. Customize Your Server

- **Add Tools**: Implement in `src/your_project/tools/`
- **Add Resources**: Implement in `src/your_project/resources/`
- **Add Prompts**: Implement in `src/your_project/prompts/`
- **Configure**: Edit `config.example.yaml`

### 4. Test and Deploy

```bash
# Run tests
pytest

# Run with Docker
docker-compose up

# Deploy
git push origin main  # Triggers CI/CD
```

## Example Server Types

### 🛠️ Tools Server

```python
@server.tool("weather_forecast")
async def get_weather(location: str, days: int = 5) -> dict:
    """Get weather forecast for a location."""
    # Your implementation here
    return {"location": location, "forecast": [...]}
```

### 📚 Resources Server

```python
@server.resource("weather://current")
async def current_weather() -> str:
    """Provide current weather data."""
    # Your implementation here
    return json.dumps(weather_data)
```

### 💬 Prompts Server

```python
@server.prompt("weather_analysis")
async def weather_analysis_prompt(data: str) -> str:
    """Generate weather analysis prompt."""
    return f"""Analyze this weather data and provide insights:
    
{data}

Please provide:
1. Current conditions summary
2. Notable weather patterns
3. Recommendations for activities
"""
```

## Configuration Options

The generated project includes extensive configuration options:

```yaml
# Server settings
host: localhost
port: 8000
log_level: INFO

# Feature toggles
enable_tools: true
enable_resources: true
enable_prompts: true

# Custom settings
custom_settings:
  debug_mode: false
  max_concurrent_requests: 10
  # Add your custom options here
```

## CLI Usage

```bash
# Generate with defaults
egile-mcp-starter --no-input

# Use custom config file
egile-mcp-starter --config-file my-config.yaml

# Specify output directory
egile-mcp-starter --output-dir ./projects/

# Verbose output
egile-mcp-starter --verbose
```

## Integration with Claude Desktop

Add your generated server to Claude Desktop configuration:

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "python",
      "args": ["/path/to/your-project/src/main.py"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`poetry run pytest`)
5. Run code quality checks (`poetry run black . && poetry run flake8 . && poetry run mypy egile_mcp_starter`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter

# Install with Poetry
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run all quality checks
poetry run black .
poetry run flake8 .
poetry run mypy egile_mcp_starter
poetry run pytest --cov=egile_mcp_starter
```

### CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline with GitHub Actions that:

- **Testing**: Runs tests across Python 3.10, 3.11, and 3.12
- **Code Quality**: Checks formatting (Black), linting (Flake8), type hints (MyPy), and import sorting (isort)
- **Security**: Scans dependencies with Safety and code with Bandit
- **Template Testing**: Validates that generated projects work correctly
- **Docker**: Builds multi-platform Docker images
- **Publishing**: Automatically publishes to PyPI on releases

The pipeline runs on:
- Every push to `main` and `develop` branches
- Every pull request to `main`
- Every release

### Docker Support

Build and run the project in Docker:

```bash
# Build the image
docker build -t egile-mcp-starter .

# Run interactively
docker run -it --rm -v $(pwd)/output:/app/output egile-mcp-starter

# Generate a project
docker run -it --rm -v $(pwd)/output:/app/output egile-mcp-starter \
  --output-dir /app/output --no-input
```

## Roadmap

- [ ] Additional server templates (database, API gateway, etc.)
- [ ] Integration with more MCP client libraries
- [ ] Advanced monitoring and observability features
- [ ] Plugin system for extensibility
- [ ] GUI-based project generator

## Requirements

- Python 3.10+
- cookiecutter
- Git (for project initialization)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 **Email**: jpoullet2000@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/jpoullet2000/egile-mcp-starter/issues)
- 📖 **MCP Documentation**: [Model Context Protocol](https://modelcontextprotocol.io/)
- 🚀 **FASTMCP**: [FASTMCP Framework](https://github.com/jlowin/fastmcp)

## Acknowledgments

- [FASTMCP](https://github.com/jlowin/fastmcp) - The amazing framework that powers the generated servers
- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol specification
- [Cookiecutter](https://cookiecutter.readthedocs.io/) - The templating engine

---

Built with ❤️ to accelerate MCP server development
