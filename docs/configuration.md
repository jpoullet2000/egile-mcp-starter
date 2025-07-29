# Configuration Options

This page describes all the configuration options available when generating a new MCP server project.

## Configuration Methods

### Interactive Prompts

When you run `egile-mcp-starter` without options, you'll be prompted for each configuration value:

```bash
egile-mcp-starter
```

### Configuration File

Create a YAML configuration file to automate project generation:

```yaml
default_context:
  project_name: "My MCP Server"
  project_slug: "my_mcp_server"
  project_description: "A comprehensive MCP server"
  author_name: "Your Name"
  author_email: "your@email.com"
  github_username: "yourusername"
  version: "0.1.0"
  python_version: "3.11"
  server_type: "full"
  use_docker: "y"
  use_github_actions: "y"
  use_pre_commit: "y"
  license: "MIT"
  include_examples: "y"
```

Use it with:

```bash
egile-mcp-starter --config-file my-config.yaml --no-input
```

### CLI Option Overrides

You can override specific configuration values using command-line options, even when using a configuration file:

```bash
# Override project name via CLI
egile-mcp-starter --config-file my-config.yaml --project-name "custom_server_name" --no-input

# Quick generation with minimal CLI options
egile-mcp-starter --project-name "my_api_server" --template mcp --no-input

# Override output directory
egile-mcp-starter --project-name "test_server" --output-dir ./build --no-input
```

**Available CLI Overrides:**
- `--project-name`: Override the project name (affects directory and package names)
- `--template`: Choose the template (`mcp`, `rag`)  
- `--output-dir`: Specify output directory
- `--verbose`: Enable detailed output

The CLI overrides take precedence over configuration file values.
```

## Configuration Options

### Project Information

#### `project_name`
- **Description**: Display name for your project
- **Type**: String
- **Default**: "My MCP Server"
- **Example**: "Weather Forecast Server"

#### `project_slug`
- **Description**: Python package name (auto-generated from project_name)
- **Type**: String (lowercase, underscores)
- **Default**: Auto-generated
- **Example**: "weather_forecast_server"

#### `project_description`
- **Description**: Brief description of your project
- **Type**: String
- **Default**: "A Model Context Protocol server built with FASTMCP"
- **Example**: "Provides weather data and forecasting tools for AI assistants"

### Author Information

#### `author_name`
- **Description**: Your full name
- **Type**: String
- **Default**: "Your Name"
- **Example**: "John Doe"

#### `author_email`
- **Description**: Your email address
- **Type**: String (email format)
- **Default**: "your.email@example.com"
- **Example**: "john.doe@example.com"

#### `github_username`
- **Description**: Your GitHub username
- **Type**: String
- **Default**: "yourusername"
- **Example**: "johndoe"

### Version Information

#### `version`
- **Description**: Initial version of your project
- **Type**: String (semantic version)
- **Default**: "0.1.0"
- **Example**: "1.0.0"

#### `python_version`
- **Description**: Python version to target
- **Type**: Choice
- **Choices**: "3.8", "3.9", "3.10", "3.11", "3.12"
- **Default**: "3.11"

### Server Configuration

#### `server_type`
- **Description**: Type of MCP server to generate
- **Type**: Choice
- **Choices**: 
  - `"tools"`: Server with tool implementations only
  - `"resources"`: Server with resource management only
  - `"prompts"`: Server with prompt templates only
  - `"full"`: Complete server with all capabilities
- **Default**: "full"

### Feature Toggles

#### `use_docker`
- **Description**: Include Docker support
- **Type**: Choice ("y" or "n")
- **Default**: "y"
- **Includes**: Dockerfile, docker-compose.yml, .dockerignore

#### `use_github_actions`
- **Description**: Include GitHub Actions CI/CD workflows
- **Type**: Choice ("y" or "n")
- **Default**: "y"
- **Includes**: .github/workflows/ci.yml

#### `use_pre_commit`
- **Description**: Include pre-commit hooks configuration
- **Type**: Choice ("y" or "n")
- **Default**: "y"
- **Includes**: .pre-commit-config.yaml

#### `include_examples`
- **Description**: Include example implementations
- **Type**: Choice ("y" or "n")
- **Default**: "y"
- **Includes**: Example tools, resources, and prompts

### License Options

#### `license`
- **Description**: License for your project
- **Type**: Choice
- **Choices**:
  - `"MIT"`: MIT License (most permissive)
  - `"Apache-2.0"`: Apache License 2.0
  - `"GPL-3.0"`: GNU General Public License v3.0
  - `"BSD-3-Clause"`: BSD 3-Clause License
  - `"None"`: No license file
- **Default**: "MIT"

## Server Types Explained

### Tools Server (`server_type: "tools"`)

Creates a server focused on providing tools that AI systems can call:

- Includes tool implementation structure
- Example tool implementations (if `include_examples: "y"`)
- Optimized for function calling and AI interactions
- No resource or prompt capabilities

**Use cases**: API integrations, data processing, calculations, external service calls

### Resources Server (`server_type: "resources"`)

Creates a server focused on providing data resources:

- Includes resource handler structure  
- Example resource implementations (if `include_examples: "y"`)
- Optimized for data access and information retrieval
- No tool or prompt capabilities

**Use cases**: Database access, file systems, data feeds, content management

### Prompts Server (`server_type: "prompts"`)

Creates a server focused on providing prompt templates:

- Includes prompt template structure
- Example prompt implementations (if `include_examples: "y"`)
- Optimized for AI guidance and instruction
- No tool or resource capabilities

**Use cases**: Prompt libraries, conversation templates, AI instruction sets

### Full Server (`server_type: "full"`)

Creates a comprehensive server with all capabilities:

- Includes tools, resources, and prompts
- Complete example implementations (if `include_examples: "y"`)
- Maximum flexibility and functionality
- All MCP capabilities enabled

**Use cases**: Complex AI assistants, comprehensive integrations, multi-purpose servers

## Advanced Configuration

### Environment Variables

You can override any configuration option using environment variables:

```bash
export COOKIECUTTER_PROJECT_NAME="My Server"
export COOKIECUTTER_AUTHOR_NAME="John Doe"
egile-mcp-starter --no-input
```

### Template Customization

For advanced users, you can modify the template itself:

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter

# Modify templates in egile_mcp_starter/template/
# Then use locally
cookiecutter ./egile_mcp_starter/template/
```

## Configuration Examples

### Minimal Tool Server

```yaml
default_context:
  project_name: "Simple Calculator"
  project_description: "Basic math operations for AI"
  author_name: "Developer"
  author_email: "dev@example.com"
  server_type: "tools"
  use_docker: "n"
  use_github_actions: "n"
  use_pre_commit: "n"
  include_examples: "y"
```

### Production-Ready Full Server

```yaml
default_context:
  project_name: "Enterprise Data Server"
  project_description: "Comprehensive data access and processing server"
  author_name: "Enterprise Team"
  author_email: "team@company.com"
  github_username: "enterprise-team"
  version: "1.0.0"
  python_version: "3.11"
  server_type: "full"
  use_docker: "y"
  use_github_actions: "y"
  use_pre_commit: "y"
  license: "Apache-2.0"
  include_examples: "y"
```

### Development/Learning Server

```yaml
default_context:
  project_name: "Learning MCP Server"
  project_description: "Educational MCP server for learning"
  author_name: "Student"
  author_email: "student@university.edu"
  server_type: "full"
  python_version: "3.12"
  use_docker: "y"
  use_github_actions: "n"
  use_pre_commit: "y"
  license: "MIT"
  include_examples: "y"
```
