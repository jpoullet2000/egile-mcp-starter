# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-07-29

### Added
- **Plugin Architecture**: Implemented extensible plugin system for template management
  - Abstract `TemplatePlugin` base class for creating custom templates
  - `TemplateRegistry` for plugin discovery and management
  - Built-in plugin discovery for templates in `egile_mcp_starter/plugins/builtin/`
  - Support for external plugin registration
- **RAG Template**: New template for Retrieval-Augmented Generation (RAG) applications
  - Multiple vector database support: Chroma, Pinecone, Weaviate, Qdrant, FAISS
  - Multiple embedding models: Sentence Transformers, OpenAI, Cohere
  - Document processing capabilities (PDF, text, web scraping)
  - Configurable chunking strategies and retrieval methods
  - Advanced search capabilities with filtering and metadata
- **Enhanced CLI**: Extended command-line interface with template selection
  - `--template` option to choose between available templates (mcp, rag)
  - `--list-templates` option to display all available templates
  - `--project-name` option to override project name and directory structure
  - Dynamic template validation and error handling
  - Improved help messages and user guidance
- **Comprehensive Documentation**: 
  - New `docs/templates.md` with plugin development guide
  - Updated README with streamlined content (reduced from 629 to 264 lines)
  - Template-specific documentation and examples
  - Plugin architecture best practices
- **Testing Suite**: Complete test coverage for plugin system
  - 28+ test methods covering all plugin functionality
  - Unit tests for template plugins, registry, and generator integration
  - Integration tests for end-to-end workflows
  - Mock-based testing for isolated component testing

### Changed
- **Generator Architecture**: Refactored `MCPProjectGenerator` to use plugin system
  - Template selection now handled through registry
  - Context generation delegated to template plugins
  - Backward compatibility maintained with original MCP template
- **Template Organization**: Restructured template system
  - Original template moved to `egile_mcp_starter/plugins/builtin/mcp_template.py`
  - New RAG template in `egile_mcp_starter/plugins/builtin/rag_template.py`
  - Template directories organized under `egile_mcp_starter/templates/`
- **Documentation Structure**: Reorganized documentation
  - Consolidated plugin architecture docs into main documentation
  - Integrated template information into README and docs

### Fixed
- CLI output formatting for project path handling
- Template path resolution in different environments
- Test compatibility with new plugin architecture
- Error handling for invalid template selections
- Project slug generation in template plugins when project name is overridden
- Plugin system context handling for custom project names

### Technical Details
- Plugin system supports hooks for pre/post generation processing
- Template validation with customizable context requirements
- Dependency computation for RAG templates based on selected features
- Registry-based plugin discovery with automatic loading
- Comprehensive error handling and user-friendly messages

## [0.1.0] - 2025-07-28

### Added
- Initial release of egile-mcp-starter
- Comprehensive cookiecutter template for MCP servers using FASTMCP framework
- Support for multiple server types: tools, resources, prompts, and full
- Interactive CLI for project generation (`egile-mcp-starter`)
- Poetry-based dependency management
- Docker support with optional docker-compose configuration
- GitHub Actions CI/CD workflows
- Pre-commit hooks for code quality
- Comprehensive test suite with pytest
- Type checking with MyPy
- Code formatting with Black
- Linting with Flake8
- YAML-based configuration with environment variable support
- Example implementations for tools, resources, and prompts
- Detailed documentation and README generation
- Support for Python 3.10, 3.11, and 3.12
- Configurable server types (tools, resources, prompts, full)
- Optional Docker and GitHub Actions integration
- Development tools integration (Black, Flake8, MyPy, pre-commit)
- License options (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause)
- Test suite with coverage reporting
- Configuration management with YAML and environment variables
