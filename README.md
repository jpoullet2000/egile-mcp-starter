# egile-mcp-starter

[![PyPI - Version](https://img.shields.io/pypi/v/egile-mcp-starter.svg)](https://pypi.org/project/egile-mcp-starter)
[![Tests](https://github.com/jpoullet2000/egile-mcp-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/jpoullet2000/egile-mcp-starter/actions/workflows/ci.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/egile-mcp-starter.svg)](https://pypi.org/project/egile-mcp-starter)
[![License](https://img.shields.io/github/license/jpoullet2000/egile-mcp-starter.svg?v=2)](https://github.com/jpoullet2000/egile-mcp-starter/blob/main/LICENSE)
[![Docker](https://img.shields.io/docker/automated/jpoullet2000/egile-mcp-starter.svg)](https://hub.docker.com/r/jpoullet2000/egile-mcp-starter)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![FastMCP](https://img.shields.io/badge/built%20with-FastMCP-green.svg)](https://github.com/jlowin/fastmcp)
[![MCP](https://img.shields.io/badge/protocol-MCP-orange.svg)](https://modelcontextprotocol.io/)
[![Documentation](https://img.shields.io/badge/docs-ReadTheDocs-blue.svg)](https://egile-mcp-starter.readthedocs.io/)

A comprehensive cookiecutter template for creating Model Context Protocol (MCP) servers using the FASTMCP framework.

📖 **[Full Documentation](https://egile-mcp-starter.readthedocs.io/)** | 🚀 **[Quick Start](#quick-start)** | 🛠️ **[Templates](#available-templates)**

## Features

- 🚀 **Modern Python Setup**: Uses Poetry for dependency management and packaging
- 🏗️ **FASTMCP Framework**: Built on the efficient FASTMCP framework for MCP servers
- � **Plugin Architecture**: Extensible template system with multiple server types
- 🛠️ **Multiple Templates**: Choose from MCP, RAG, or custom templates
- 🧪 **Testing Ready**: Comprehensive test suite with pytest and coverage
- 🔧 **Development Tools**: Pre-configured with Black, Flake8, MyPy, and pre-commit hooks
- 🐳 **Docker Support**: Optional Docker configuration for easy deployment
- 🔄 **CI/CD Ready**: GitHub Actions workflows for automated testing and deployment
- 📚 **Rich Documentation**: Detailed README and code documentation
- 🎛️ **Configurable**: YAML-based configuration with environment variable support

## Quick Start

### Installation

```bash
# Install with pip (recommended)
pip install egile-mcp-starter

# Or use Docker
docker pull jpoullet2000/egile-mcp-starter
docker run -it jpoullet2000/egile-mcp-starter

# Or install from source
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter
poetry install
```

### Generate a New MCP Server

```bash
# Using the installed command (default MCP template)
egile-mcp-starter

# Or if installed from source
poetry run egile-mcp-starter

# Choose a specific template
egile-mcp-starter --template rag

# List available templates
egile-mcp-starter --list-templates

# With custom project name
egile-mcp-starter --project-name "my_custom_server"

# With multiple options
egile-mcp-starter --template rag --output-dir ./my-projects --project-name "my_rag_server" --verbose
```

### CLI Options

The `egile-mcp-starter` command supports the following options:

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--template` | `-t` | Choose the template to use | `--template rag` |
| `--project-name` | | Override the project name (affects directory and package name) | `--project-name "my_server"` |
| `--output-dir` | `-o` | Output directory for the generated project | `--output-dir ./projects` |
| `--list-templates` | | List all available templates and exit | `--list-templates` |
| `--verbose` | `-v` | Print detailed status information | `--verbose` |
| `--no-input` | | Don't prompt for parameters, use defaults | `--no-input` |
| `--config-file` | | Path to cookiecutter config file | `--config-file config.yaml` |
| `--default-config` | | Use default values for all template variables | `--default-config` |
| `--help` | | Show help message and exit | `--help` |

**Examples:**

```bash
# Generate with custom name and template
egile-mcp-starter --template rag --project-name "my_awesome_rag_server"

# Non-interactive generation for CI/CD
egile-mcp-starter --no-input --project-name "test_server" --output-dir ./build

# List available templates
egile-mcp-starter --list-templates
```

### Available Templates

The egile-mcp-starter uses a **plugin architecture** that supports multiple project templates. Choose the template that best fits your needs:

#### 🔧 MCP Template (default)
The standard MCP server template with comprehensive features:
- **Server Types**: Tools, resources, prompts, or full-featured servers
- **FASTMCP Integration**: Built on the efficient FASTMCP framework
- **Development Ready**: Testing, linting, CI/CD, Docker support
- **Flexible Configuration**: YAML-based config with environment variables

```bash
egile-mcp-starter --template mcp
```

#### 🧠 RAG Template
Advanced RAG-enabled MCP server with vector search capabilities:
- **Vector Databases**: Chroma, Pinecone, Weaviate, Qdrant, FAISS support
- **Embedding Models**: Sentence Transformers, OpenAI, Cohere
- **Document Processing**: PDF, DOCX, Excel, text files
- **Web Scraping**: Optional web page scraping and indexing
- **Chunking Strategies**: Recursive, semantic, fixed-size
- **Reranking**: Optional result reranking for better relevance
- **MCP Tools**: `ingest_documents`, `search_documents`, `scrape_and_index`
- **MCP Resources**: Document listing, metadata access, chunk search

```bash
egile-mcp-starter --template rag
```

#### 🔌 Plugin System Features
- **Extensible**: Easy to add new templates without modifying core code
- **External Plugins**: Third-party templates via entry points
- **Template Hooks**: Pre/post-generation customization
- **Backward Compatible**: Original functionality preserved

```bash
# List all available templates
egile-mcp-starter --list-templates

# Generate with specific template and options
egile-mcp-starter --template rag --output-dir ./my-projects --project-name "my_rag_server" --verbose
```

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

## Extending the Plugin System

### Adding Custom Templates

The plugin architecture makes it easy to add new templates:

1. **Create a Template Plugin**:
```python
from egile_mcp_starter import TemplatePlugin
from pathlib import Path

class MyTemplatePlugin(TemplatePlugin):
    def __init__(self):
        super().__init__(
            name="my_template",
            description="My custom MCP server template",
            version="1.0.0"
        )
    
    def get_template_path(self) -> Path:
        return Path(__file__).parent / "my_template"
    
    def get_default_context(self) -> dict:
        return {"project_name": "My Custom Server"}
```

2. **Register the Plugin**:
```python
from egile_mcp_starter import get_registry

registry = get_registry()
registry.register(MyTemplatePlugin())
```

3. **External Plugin Distribution**:
```python
# In your package's setup.py or pyproject.toml
entry_points = {
    'egile_mcp_starter.templates': [
        'my_template = my_package.my_template:MyTemplatePlugin',
    ],
}
```

### Template Hooks

Customize the generation process with hooks:
- **Pre-generation**: Modify context, validate inputs, compute dependencies
- **Post-generation**: Initialize databases, download models, set up git repos

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

## Documentation

📖 **[Complete Documentation](https://egile-mcp-starter.readthedocs.io/)** - Full documentation hosted on ReadTheDocs

The documentation includes:

- **[Installation Guide](https://egile-mcp-starter.readthedocs.io/en/latest/installation.html)**: Detailed installation instructions
- **[Quick Start](https://egile-mcp-starter.readthedocs.io/en/latest/quickstart.html)**: Get up and running quickly
- **[Configuration](https://egile-mcp-starter.readthedocs.io/en/latest/configuration.html)**: Detailed configuration options
- **[Server Types](https://egile-mcp-starter.readthedocs.io/en/latest/server_types.html)**: Available templates and their features
- **[API Reference](https://egile-mcp-starter.readthedocs.io/en/latest/api_reference.html)**: Complete API documentation
- **[Contributing](https://egile-mcp-starter.readthedocs.io/en/latest/contributing.html)**: How to contribute to the project

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

- � **Documentation**: [egile-mcp-starter.readthedocs.io](https://egile-mcp-starter.readthedocs.io/)
- �📧 **Email**: jpoullet2000@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/jpoullet2000/egile-mcp-starter/issues)
- 📖 **MCP Documentation**: [Model Context Protocol](https://modelcontextprotocol.io/)
- 🚀 **FASTMCP**: [FASTMCP Framework](https://github.com/jlowin/fastmcp)

## Acknowledgments

- [FASTMCP](https://github.com/jlowin/fastmcp) - The amazing framework that powers the generated servers
- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol specification
- [Cookiecutter](https://cookiecutter.readthedocs.io/) - The templating engine

---

Built with ❤️ to accelerate MCP server development
