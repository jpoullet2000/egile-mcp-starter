# Installation

## Prerequisites

- Python 3.10 or higher
- Git (for project initialization)

## Install from PyPI

The easiest way to install egile-mcp-starter is from PyPI:

```bash
pip install egile-mcp-starter
```

## Install from Source

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter

# Install with Poetry (recommended)
poetry install

# Or install with pip
pip install -e .
```

## Development Installation

If you want to contribute to the project:

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-starter.git
cd egile-mcp-starter

# Install with development dependencies
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install
```

## Verify Installation

After installation, verify that egile-mcp-starter is working:

```bash
# Check version
egile-mcp-starter --version

# Show help
egile-mcp-starter --help
```

## Docker Installation

You can also use the Docker image:

```bash
# Pull the image
docker pull jpoullet2000/egile-mcp-starter:latest

# Run interactively
docker run -it --rm -v $(pwd)/output:/app/output jpoullet2000/egile-mcp-starter

# Generate a project
docker run -it --rm -v $(pwd)/output:/app/output jpoullet2000/egile-mcp-starter \
  --output-dir /app/output --no-input
```

## Troubleshooting

### Common Issues

**Command not found after installation**

If you get a "command not found" error, make sure your Python scripts directory is in your PATH:

```bash
# For pip installations
export PATH="$HOME/.local/bin:$PATH"

# For Poetry installations
poetry shell
```

**Python version compatibility**

Ensure you're using Python 3.10 or higher:

```bash
python --version
```

**Poetry not found**

If you don't have Poetry installed:

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```
