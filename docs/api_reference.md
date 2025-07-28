# API Reference

This section provides detailed API documentation for the egile-mcp-starter codebase.

## Command Line Interface

```{eval-rst}
.. automodule:: egile_mcp_starter.cli
   :members:
   :undoc-members:
   :show-inheritance:
```

## Generator Module

```{eval-rst}
.. automodule:: egile_mcp_starter.generator
   :members:
   :undoc-members:
   :show-inheritance:
```

## CLI Functions

### main()

The main entry point for the egile-mcp-starter command line interface.

**Usage:**
```bash
egile-mcp-starter [OPTIONS]
```

**Options:**
- `--output-dir TEXT`: Output directory for the generated project
- `--config-file TEXT`: Configuration file path
- `--no-input`: Don't prompt for input, use defaults
- `--verbose`: Enable verbose output
- `--version`: Show version and exit
- `--help`: Show help message and exit

**Examples:**
```bash
# Interactive mode
egile-mcp-starter

# With configuration file
egile-mcp-starter --config-file my-config.yaml --no-input

# Specify output directory
egile-mcp-starter --output-dir ./my-projects
```

## Generator Functions

### generate_mcp_server()

Generates a new MCP server project using the cookiecutter template.

**Parameters:**
- `output_dir` (str, optional): Output directory path
- `config_file` (str, optional): Configuration file path
- `no_input` (bool): Skip interactive prompts
- `extra_context` (dict, optional): Additional template context

**Returns:**
- `str`: Path to the generated project

**Raises:**
- `ProjectGenerationError`: If project generation fails
- `TemplateError`: If template processing fails

**Example:**
```python
from egile_mcp_starter.generator import generate_mcp_server

# Generate with defaults
project_path = generate_mcp_server()

# Generate with custom options
project_path = generate_mcp_server(
    output_dir="./projects",
    no_input=True,
    extra_context={
        "project_name": "My Server",
        "server_type": "tools"
    }
)
```

## Template Context Variables

The following variables are available in the cookiecutter template:

### Project Configuration
- `cookiecutter.project_name`: Display name for the project
- `cookiecutter.project_slug`: Python package name
- `cookiecutter.project_description`: Project description
- `cookiecutter.version`: Initial project version

### Author Information
- `cookiecutter.author_name`: Author's full name
- `cookiecutter.author_email`: Author's email address
- `cookiecutter.github_username`: GitHub username

### Technical Configuration
- `cookiecutter.python_version`: Target Python version
- `cookiecutter.server_type`: MCP server type (tools/resources/prompts/full)

### Feature Flags
- `cookiecutter.use_docker`: Include Docker support (y/n)
- `cookiecutter.use_github_actions`: Include GitHub Actions (y/n)
- `cookiecutter.use_pre_commit`: Include pre-commit hooks (y/n)
- `cookiecutter.include_examples`: Include example implementations (y/n)

### License
- `cookiecutter.license`: Project license type

## Exception Classes

### ProjectGenerationError

Raised when project generation fails.

**Attributes:**
- `message`: Error description
- `context`: Additional error context

**Example:**
```python
try:
    generate_mcp_server()
except ProjectGenerationError as e:
    print(f"Generation failed: {e.message}")
    print(f"Context: {e.context}")
```

### TemplateError

Raised when template processing encounters an error.

**Attributes:**
- `template_path`: Path to the problematic template
- `error_details`: Detailed error information

## Configuration Schema

### YAML Configuration File Format

```yaml
default_context:
  # Project information
  project_name: "My MCP Server"
  project_slug: "my_mcp_server"  # Optional, auto-generated
  project_description: "A comprehensive MCP server"
  version: "0.1.0"
  
  # Author information
  author_name: "Your Name"
  author_email: "your@email.com"
  github_username: "yourusername"
  
  # Technical configuration
  python_version: "3.11"  # 3.8, 3.9, 3.10, 3.11, 3.12
  server_type: "full"     # tools, resources, prompts, full
  
  # Features
  use_docker: "y"           # y or n
  use_github_actions: "y"   # y or n
  use_pre_commit: "y"       # y or n
  include_examples: "y"     # y or n
  
  # License
  license: "MIT"  # MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, None
```

## Environment Variables

The following environment variables can override configuration:

- `COOKIECUTTER_PROJECT_NAME`: Override project name
- `COOKIECUTTER_AUTHOR_NAME`: Override author name
- `COOKIECUTTER_AUTHOR_EMAIL`: Override author email
- `COOKIECUTTER_GITHUB_USERNAME`: Override GitHub username
- `COOKIECUTTER_SERVER_TYPE`: Override server type
- `COOKIECUTTER_PYTHON_VERSION`: Override Python version
- `COOKIECUTTER_USE_DOCKER`: Override Docker usage
- `COOKIECUTTER_USE_GITHUB_ACTIONS`: Override GitHub Actions usage
- `COOKIECUTTER_LICENSE`: Override license choice

## Template Hooks

The template includes pre and post generation hooks:

### Pre-generation Hook

Validates configuration and prepares the environment:

- Validates Python version compatibility
- Checks required dependencies
- Prepares template context

### Post-generation Hook

Performs cleanup and initialization:

- Initializes Git repository
- Sets up pre-commit hooks (if enabled)
- Creates initial commit
- Displays success message

## Return Values

### Success

When generation succeeds, functions return the path to the generated project:

```python
"/path/to/output/my_mcp_server"
```

### Error Handling

All functions use proper exception handling:

```python
try:
    project_path = generate_mcp_server()
    print(f"✅ Project created at: {project_path}")
except ProjectGenerationError as e:
    print(f"❌ Generation failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

## Logging

The package uses Python's logging module:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Generate project with debug output
generate_mcp_server(verbose=True)
```

Log levels:
- `DEBUG`: Detailed debugging information
- `INFO`: General information about operations
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failures

## Version Information

Access version information programmatically:

```python
from egile_mcp_starter import __version__
print(f"egile-mcp-starter version: {__version__}")
```

## Compatibility

### Python Versions
- **Minimum**: Python 3.10
- **Tested**: Python 3.10, 3.11, 3.12
- **Recommended**: Python 3.11

### Dependencies
- `cookiecutter >= 2.1.1`
- `jinja2 >= 3.0.0`
- `click >= 8.0.0`
- `pyyaml >= 6.0`
