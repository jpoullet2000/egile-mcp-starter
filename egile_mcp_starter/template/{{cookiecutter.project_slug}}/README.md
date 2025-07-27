# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Overview

This is a Model Context Protocol (MCP) server built with the [FASTMCP](https://github.com/jlowin/fastmcp) framework. MCP is a standardized protocol for communication between AI systems and external tools/data sources.

## Features

- 🚀 Built with FASTMCP for rapid development
- 🛠️ {% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" %}Tool support for AI interactions{% endif %}
- 📚 {% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" %}Resource management for data access{% endif %}
- 💬 {% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" %}Prompt templates for AI guidance{% endif %}
- 🧪 Comprehensive testing suite
- 📋 Type hints throughout
- 🔧 Development tools (linting, formatting, pre-commit hooks)
{% if cookiecutter.use_docker == "y" -%}
- 🐳 Docker support for easy deployment
{% endif -%}
{% if cookiecutter.use_github_actions == "y" -%}
- 🔄 GitHub Actions CI/CD pipeline
{% endif %}

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}

# Install dependencies with Poetry
poetry install

# Or install with development dependencies
poetry install --with dev
```

### Usage

#### Running the Server

```bash
# Run the MCP server using Poetry
poetry run python src/main.py

# Or activate the virtual environment first
poetry shell
python src/main.py

# Or use the installed command
poetry run {{ cookiecutter.project_slug.replace('_', '-') }}
```

#### Configuration

The server can be configured through environment variables or a configuration file:

```bash
# Set environment variables
export MCP_SERVER_HOST=localhost
export MCP_SERVER_PORT=8000
export LOG_LEVEL=INFO

# Run with custom config
poetry run python src/main.py --config config.yaml
```

#### Using with Claude Desktop

Add this server to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "poetry",
      "args": ["run", "python", "/path/to/{{ cookiecutter.project_slug }}/src/main.py"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

{% if cookiecutter.use_docker == "y" -%}
### Docker Usage

```bash
# Build the image
docker build -t {{ cookiecutter.project_slug }} .

# Run the container
docker run -p 8000:8000 {{ cookiecutter.project_slug }}
```
{% endif %}

## Development

### Setup Development Environment

```bash
# Install development dependencies
poetry install --with dev

{% if cookiecutter.use_pre_commit == "y" -%}
# Install pre-commit hooks
poetry run pre-commit install
{% endif %}
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/test_server.py -v
```

### Code Quality

```bash
# Format code
poetry run black src tests

# Check linting
poetry run flake8 src tests

# Type checking
poetry run mypy src

{% if cookiecutter.use_pre_commit == "y" -%}
# Run all pre-commit checks
poetry run pre-commit run --all-files
{% endif %}

# Add new dependencies
poetry add <package-name>

# Add development dependencies
poetry add --group dev <package-name>
```

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/
│   ├── {{ cookiecutter.project_slug }}/
│   │   ├── __init__.py
│   │   ├── server.py          # Main MCP server implementation
│   │   ├── config.py          # Configuration management
{% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
│   │   ├── tools/             # Tool implementations
│   │   │   ├── __init__.py
│   │   │   └── example_tools.py
{% endif -%}
{% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
│   │   ├── resources/         # Resource handlers
│   │   │   ├── __init__.py
│   │   │   └── example_resources.py
{% endif -%}
{% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
│   │   ├── prompts/           # Prompt templates
│   │   │   ├── __init__.py
│   │   │   └── example_prompts.py
{% endif -%}
│   │   └── utils.py           # Utility functions
│   └── main.py                # Entry point
├── tests/
│   ├── __init__.py
│   ├── test_server.py
{% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
│   ├── test_tools.py
{% endif -%}
{% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
│   ├── test_resources.py
{% endif -%}
{% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
│   ├── test_prompts.py
{% endif -%}
│   └── conftest.py
{% if cookiecutter.use_docker == "y" -%}
├── Dockerfile
├── docker-compose.yml
{% endif -%}
├── pyproject.toml
├── poetry.lock
├── README.md
{% if cookiecutter.license != "None" -%}
├── LICENSE
{% endif -%}
{% if cookiecutter.use_github_actions == "y" -%}
└── .github/
    └── workflows/
        └── ci.yml
{% endif %}
```

## MCP Server Capabilities

This server implements the following MCP capabilities:

{% if cookiecutter.server_type == "tools" or cookiecutter.server_type == "full" -%}
### Tools

- **example_tool**: A sample tool that demonstrates basic functionality
- Add your custom tools in `src/{{ cookiecutter.project_slug }}/tools/`

{% endif -%}
{% if cookiecutter.server_type == "resources" or cookiecutter.server_type == "full" -%}
### Resources

- **example_resource**: A sample resource for data access
- Add your custom resources in `src/{{ cookiecutter.project_slug }}/resources/`

{% endif -%}
{% if cookiecutter.server_type == "prompts" or cookiecutter.server_type == "full" -%}
### Prompts

- **example_prompt**: A sample prompt template
- Add your custom prompts in `src/{{ cookiecutter.project_slug }}/prompts/`

{% endif %}
## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

{% if cookiecutter.license == "MIT" -%}
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
{% elif cookiecutter.license == "Apache-2.0" -%}
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
{% elif cookiecutter.license == "GPL-3.0" -%}
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
{% elif cookiecutter.license == "BSD-3-Clause" -%}
This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.
{% else -%}
All rights reserved.
{% endif %}

## Support

- 📧 Email: {{ cookiecutter.author_email }}
- 🐛 Issues: [GitHub Issues](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues)
- 📖 Documentation: [MCP Documentation](https://modelcontextprotocol.io/)
- 🚀 FASTMCP: [FASTMCP Documentation](https://github.com/jlowin/fastmcp)

---

Built with ❤️ using [FASTMCP](https://github.com/jlowin/fastmcp) and the [Model Context Protocol](https://modelcontextprotocol.io/).
