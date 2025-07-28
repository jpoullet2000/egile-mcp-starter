# Quick Start

This guide will help you create your first MCP server using egile-mcp-starter.

## Generate Your First MCP Server

### Interactive Mode

The simplest way to get started is to run the command interactively:

```bash
egile-mcp-starter
```

You'll be prompted for various configuration options:

```
project_name [My MCP Server]: Weather MCP Server
project_description [A Model Context Protocol server built with FASTMCP]: Weather data MCP server with forecast tools
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
github_username [yourusername]: johndoe
server_type [full]: tools
python_version [3.11]: 3.11
use_docker [y]: y
use_github_actions [y]: y
include_examples [y]: y
```

### Non-Interactive Mode

For automation or CI/CD, you can use the `--no-input` flag with a configuration file:

```bash
# Create a config file
cat > my-config.yaml << 'EOF'
default_context:
  project_name: "My Weather Server"
  project_slug: "my_weather_server"
  project_description: "A MCP server for weather data"
  author_name: "Your Name"
  author_email: "your@email.com"
  github_username: "yourusername"
  server_type: "tools"
  python_version: "3.11"
  use_docker: "y"
  use_github_actions: "y"
  include_examples: "y"
EOF

# Generate project
egile-mcp-starter --config-file my-config.yaml --no-input
```

## Project Structure

After generation, your project will have this structure:

```
my_weather_server/
├── src/
│   ├── my_weather_server/
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
├── pyproject.toml             # Project configuration
└── README.md                  # Project documentation
```

## Set Up Your Development Environment

Navigate to your new project:

```bash
cd my_weather_server
```

Install dependencies:

```bash
# With Poetry (recommended)
poetry install

# Or with pip
pip install -e ".[dev]"
```

If you enabled pre-commit hooks:

```bash
poetry run pre-commit install
```

## Run Your Server

Start your MCP server:

```bash
# With Poetry
poetry run python src/main.py

# Or activate the virtual environment
poetry shell
python src/main.py
```

## Test Your Server

Run the test suite:

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html
```

## Code Quality Checks

Format and check your code:

```bash
# Format code
poetry run black src tests

# Check linting
poetry run flake8 src tests

# Type checking
poetry run mypy src

# Run all pre-commit checks
poetry run pre-commit run --all-files
```

## Docker Support

If you enabled Docker support:

```bash
# Build the image
docker build -t my-weather-server .

# Run with docker-compose
docker-compose up
```

## Next Steps

1. **Customize your server**: Edit the files in `src/my_weather_server/`
2. **Add your tools**: Implement custom tools in `src/my_weather_server/tools/`
3. **Configure settings**: Edit `config.example.yaml`
4. **Write tests**: Add tests in the `tests/` directory
5. **Deploy**: Use the included Docker and CI/CD configurations

## Integration with Claude Desktop

To use your server with Claude Desktop, add it to your configuration:

```json
{
  "mcpServers": {
    "my-weather-server": {
      "command": "poetry",
      "args": ["run", "python", "/path/to/my_weather_server/src/main.py"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## CLI Options

### Common Options

- `--output-dir DIR`: Specify output directory (default: current directory)
- `--config-file FILE`: Use a configuration file
- `--no-input`: Don't prompt for input (use defaults or config file)
- `--verbose`: Enable verbose output
- `--version`: Show version information
- `--help`: Show help message

### Examples

```bash
# Generate in a specific directory
egile-mcp-starter --output-dir ./my-projects

# Use custom configuration
egile-mcp-starter --config-file custom-config.yaml

# Automated generation
egile-mcp-starter --no-input --output-dir ./servers

# Verbose output for debugging
egile-mcp-starter --verbose
```
