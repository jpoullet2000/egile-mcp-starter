# Contributing

We welcome contributions to egile-mcp-starter! This guide will help you get started with contributing to the project.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Git for version control

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/egile-mcp-starter.git
   cd egile-mcp-starter
   ```

3. **Install development dependencies**:
   ```bash
   poetry install --with dev
   ```

4. **Install pre-commit hooks**:
   ```bash
   poetry run pre-commit install
   ```

5. **Verify the setup**:
   ```bash
   poetry run pytest
   poetry run egile-mcp-starter --version
   ```

## Development Workflow

### Creating a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/amazing-feature

# Or for bug fixes
git checkout -b fix/bug-description
```

### Making Changes

1. **Make your changes** to the codebase
2. **Add tests** for new functionality
3. **Update documentation** as needed
4. **Run the test suite**:
   ```bash
   poetry run pytest
   ```

### Code Quality

Before committing, ensure your code meets our quality standards:

```bash
# Format code with Black
poetry run black .

# Sort imports with isort
poetry run isort .

# Check linting with Flake8
poetry run flake8 egile_mcp_starter tests

# Type checking with MyPy
poetry run mypy egile_mcp_starter

# Run all pre-commit checks
poetry run pre-commit run --all-files
```

### Testing Your Changes

#### Run the Test Suite

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=egile_mcp_starter --cov-report=html

# Run specific test files
poetry run pytest tests/test_generator.py -v
```

#### Test Template Generation

```bash
# Test generating different server types
poetry run egile-mcp-starter --no-input --output-dir /tmp/test-tools
cd /tmp/test-tools/my_mcp_server
poetry install
poetry run pytest
```

#### Manual Testing

Test the CLI with various configurations:

```bash
# Test interactive mode
poetry run egile-mcp-starter

# Test with config file
echo 'default_context:
  project_name: "Test Server"
  server_type: "tools"' > test-config.yaml
poetry run egile-mcp-starter --config-file test-config.yaml --no-input
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Environment information** (OS, Python version, etc.)
- **Error messages** or logs

**Template:**
```markdown
## Bug Description
Brief description of the bug.

## Steps to Reproduce
1. Run command X
2. Configure Y
3. See error

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: Ubuntu 22.04
- Python: 3.11.0
- egile-mcp-starter: 0.1.0

## Additional Context
Any other relevant information.
```

### Feature Requests

For new features, please provide:

- **Clear description** of the feature
- **Use case** and motivation
- **Proposed implementation** (if you have ideas)
- **Alternatives considered**

### Code Contributions

We welcome:

- **Bug fixes**
- **New features**
- **Documentation improvements**
- **Template enhancements**
- **Test improvements**
- **Performance optimizations**

## Project Structure

Understanding the project structure will help with contributions:

```
egile-mcp-starter/
├── egile_mcp_starter/          # Main package
│   ├── __init__.py
│   ├── cli.py                  # Command line interface
│   ├── generator.py            # Project generation logic
│   └── template/               # Cookiecutter template
│       ├── cookiecutter.json   # Template configuration
│       └── {{cookiecutter.project_slug}}/  # Generated project template
├── tests/                      # Test suite
│   ├── test_cli.py
│   ├── test_generator.py
│   └── test_package.py
├── docs/                       # Documentation
├── pyproject.toml             # Project configuration
├── README.md
└── CHANGELOG.md
```

### Key Components

- **`cli.py`**: Command line interface using Click
- **`generator.py`**: Core logic for project generation
- **`template/`**: Cookiecutter template files
- **`tests/`**: Comprehensive test suite
- **`docs/`**: Sphinx documentation

## Template Development

### Adding New Template Features

1. **Modify the template** in `egile_mcp_starter/template/`
2. **Update `cookiecutter.json`** with new configuration options
3. **Add conditional logic** using Jinja2 templates
4. **Test the changes** with different configurations
5. **Update documentation**

### Template File Structure

```
template/
├── cookiecutter.json           # Configuration schema
└── {{cookiecutter.project_slug}}/
    ├── src/
    │   └── {{cookiecutter.project_slug}}/
    │       ├── server.py       # Uses Jinja2 conditionals
    │       ├── tools/          # {% if server_type includes tools %}
    │       ├── resources/      # {% if server_type includes resources %}
    │       └── prompts/        # {% if server_type includes prompts %}
    ├── tests/
    ├── pyproject.toml         # Template variables
    └── README.md              # Generated documentation
```

### Testing Template Changes

```bash
# Generate test projects
poetry run egile-mcp-starter --no-input --output-dir /tmp/test-full
poetry run egile-mcp-starter --no-input --output-dir /tmp/test-tools \
  --extra-context '{"server_type": "tools"}'

# Verify generated projects work
cd /tmp/test-full/my_mcp_server
poetry install && poetry run pytest

cd /tmp/test-tools/my_mcp_server  
poetry install && poetry run pytest
```

## Documentation

### Writing Documentation

- Use **Markdown** for most documentation
- Follow the **existing style** and structure
- Include **code examples** where appropriate
- Add **cross-references** to related sections

### Building Documentation

```bash
# Install documentation dependencies
poetry install --with docs

# Build documentation
cd docs
poetry run sphinx-build -b html . _build/html

# Serve locally
poetry run python -m http.server 8000 --directory _build/html
```

### Documentation Guidelines

- **Clear headings** and structure
- **Code examples** with proper syntax highlighting
- **Cross-references** using Sphinx directives
- **Screenshots** for UI elements (if applicable)
- **API documentation** using autodoc

## Testing Guidelines

### Writing Tests

- **Follow pytest conventions**
- **Use descriptive test names**
- **Test both success and failure cases**
- **Mock external dependencies**
- **Maintain high test coverage**

### Test Categories

1. **Unit tests**: Test individual functions and classes
2. **Integration tests**: Test component interactions
3. **End-to-end tests**: Test complete workflows
4. **Template tests**: Test generated project functionality

### Example Test

```python
def test_generate_tools_server(tmp_path):
    """Test generating a tools-only server."""
    output_dir = tmp_path / "output"
    
    result = generate_mcp_server(
        output_dir=str(output_dir),
        no_input=True,
        extra_context={"server_type": "tools"}
    )
    
    project_path = Path(result)
    assert project_path.exists()
    assert (project_path / "src" / "my_mcp_server" / "tools").exists()
    assert not (project_path / "src" / "my_mcp_server" / "resources").exists()
```

## Submitting Changes

### Pull Request Process

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```

2. **Create a pull request** on GitHub

3. **Fill out the PR template** with:
   - Description of changes
   - Related issues
   - Testing performed
   - Breaking changes (if any)

4. **Respond to review feedback**

5. **Squash commits** if requested

### Pull Request Template

```markdown
## Description
Brief description of the changes.

## Related Issues
Fixes #123
Closes #456

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added new tests
- [ ] All tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Creating a Release

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md**
3. **Create a pull request** with version changes
4. **Merge to main** after review
5. **Create a GitHub release** with tag
6. **CI/CD pipeline** handles publishing

## Code Style

### Python Style Guide

- Follow **PEP 8** guidelines
- Use **Black** for code formatting
- Use **isort** for import sorting
- Maximum line length: **88 characters**
- Use **type hints** for all functions

### Documentation Style

- Use **Google-style docstrings**
- Include **parameter types** and descriptions
- Add **usage examples** where helpful
- Use **Markdown** for README files

### Example Code Style

```python
from typing import Optional, Dict, Any

def generate_project(
    output_dir: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    verbose: bool = False
) -> str:
    """Generate a new MCP server project.
    
    Args:
        output_dir: Directory to create the project in
        config: Configuration overrides
        verbose: Enable verbose output
        
    Returns:
        Path to the generated project
        
    Raises:
        ProjectGenerationError: If generation fails
        
    Example:
        >>> project_path = generate_project(
        ...     output_dir="/tmp",
        ...     config={"server_type": "tools"}
        ... )
        >>> print(f"Project created at: {project_path}")
    """
    # Implementation here
    pass
```

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: jpoullet2000@gmail.com for direct contact

## Recognition

Contributors are recognized in:

- **CHANGELOG.md**: For significant contributions
- **GitHub contributors page**: Automatic recognition
- **Documentation**: For major contributions

Thank you for contributing to egile-mcp-starter! 🎉
