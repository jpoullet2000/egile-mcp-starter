# Templates and Plugin System

The egile-mcp-starter uses a powerful plugin architecture that supports multiple project templates. This document provides detailed information about available templates and how to extend the system.

## Available Templates

### MCP Template (default)

The standard MCP server template provides a solid foundation for building MCP servers:

**Features:**
- Standard MCP server with tools, resources, and prompts
- Full FASTMCP framework integration  
- Comprehensive testing suite with pytest
- Development tools (Black, Flake8, MyPy, pre-commit)
- Docker and docker-compose support
- GitHub Actions CI/CD workflows
- Multiple license options

**Server Types:**
- `tools`: Server with tool implementations for AI interactions
- `resources`: Server with resource management for data access
- `prompts`: Server with prompt templates for AI guidance  
- `full`: Complete server with all capabilities

**Usage:**
```bash
egile-mcp-starter --template mcp
```

### RAG Template

The RAG template creates advanced MCP servers with vector search and document processing capabilities:

**Features:**
- Vector database integration (Chroma, Pinecone, Weaviate, Qdrant, FAISS)
- Multiple embedding models (Sentence Transformers, OpenAI, Cohere)
- Document processing (PDF, DOCX, Excel, text files)
- Web scraping capabilities
- Configurable chunking strategies (recursive, semantic, fixed-size)
- Optional reranking for improved relevance
- Comprehensive configuration system

**Generated MCP Tools:**
- `ingest_documents`: Add documents to the vector database
- `search_documents`: Semantic search with optional reranking
- `get_document_chunks`: Retrieve specific document chunks
- `scrape_and_index`: Web scraping and indexing (if enabled)

**Generated MCP Resources:**
- `documents://list`: List all indexed documents
- `documents://metadata/{doc_id}`: Get document metadata
- `chunks://search?q={query}`: Search document chunks

**Configuration Options:**

| Option | Description | Choices |
|--------|-------------|---------|
| `vector_db` | Vector database to use | chroma, pinecone, weaviate, qdrant, faiss |
| `embedding_model` | Embedding model provider | sentence-transformers, openai, cohere |
| `document_loaders` | Include document loaders | y/n |
| `web_scraping` | Include web scraping | y/n |
| `pdf_processing` | Include PDF processing | y/n |
| `chunk_strategy` | Text chunking strategy | recursive, semantic, fixed |
| `include_reranker` | Include reranking | y/n |

**Usage:**
```bash
egile-mcp-starter --template rag
```

## Plugin Architecture

### Core Components

#### 1. TemplatePlugin Base Class

All templates inherit from the `TemplatePlugin` abstract base class:

```python
from egile_mcp_starter.plugins.base import TemplatePlugin

class MyTemplate(TemplatePlugin):
    def get_template_path(self) -> Path:
        """Return path to cookiecutter template directory"""
        
    def get_default_context(self) -> Dict[str, Any]:
        """Return default template variables"""
        
    def get_supported_features(self) -> List[str]:
        """Return list of supported features"""
        
    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate template context"""
        
    def pre_generate_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Called before project generation"""
        
    def post_generate_hook(self, project_path: Path, context: Dict[str, Any]) -> None:
        """Called after project generation"""
```

#### 2. Template Registry

The registry manages all available templates:

```python
from egile_mcp_starter import get_registry

registry = get_registry()

# List available templates
templates = registry.list_plugins()

# Get specific template
template = registry.get_plugin("rag")

# Register new template
registry.register(MyTemplatePlugin())
```

### Creating Custom Templates

#### Step 1: Create Template Plugin

```python
from pathlib import Path
from typing import Any, Dict, List
from egile_mcp_starter.plugins.base import TemplatePlugin

class DatabaseTemplatePlugin(TemplatePlugin):
    def __init__(self):
        super().__init__(
            name="database",
            description="MCP server with database connectivity",
            version="1.0.0"
        )
    
    def get_template_path(self) -> Path:
        return Path(__file__).parent / "database_template"
    
    def get_default_context(self) -> Dict[str, Any]:
        return {
            "project_name": "My Database MCP Server",
            "database_type": "postgresql",
            "include_migrations": "y",
            "use_sqlalchemy": "y"
        }
    
    def get_supported_features(self) -> List[str]:
        return ["database", "migrations", "orm", "connection_pooling"]
    
    def validate_context(self, context: Dict[str, Any]) -> bool:
        required = ["project_name", "database_type"]
        return all(field in context for field in required)
    
    def pre_generate_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Add database-specific dependencies
        db_type = context.get("database_type")
        if db_type == "postgresql":
            context["_db_driver"] = "psycopg2"
        elif db_type == "mysql":
            context["_db_driver"] = "pymysql"
        return context
    
    def post_generate_hook(self, project_path: Path, context: Dict[str, Any]) -> None:
        # Could initialize database schema, create config files, etc.
        pass
```

#### Step 2: Create Cookiecutter Template

Create the template directory structure:
```
database_template/
├── cookiecutter.json
└── {{cookiecutter.project_slug}}/
    ├── src/
    │   └── {{cookiecutter.project_slug}}/
    │       ├── __init__.py
    │       ├── server.py
    │       └── database.py
    ├── config.example.yaml
    └── README.md
```

#### Step 3: Register Template

For built-in templates, add to the registry:
```python
# In plugins/registry.py
from .builtin.database_template import DatabaseTemplatePlugin
self.register(DatabaseTemplatePlugin())
```

### External Plugins

Third-party templates can be distributed as separate packages:

#### Package Structure
```
my_mcp_templates/
├── setup.py
├── my_mcp_templates/
│   ├── __init__.py
│   └── api_template.py
└── templates/
    └── api/
        └── cookiecutter.json
```

#### Entry Points Configuration
```python
# setup.py
from setuptools import setup

setup(
    name="my-mcp-templates",
    entry_points={
        'egile_mcp_starter.templates': [
            'api = my_mcp_templates.api_template:APITemplatePlugin',
        ],
    },
)
```

#### Installation and Usage
```bash
# Install the external template package
pip install my-mcp-templates

# The template will be automatically discovered
egile-mcp-starter --list-templates

# Use the external template
egile-mcp-starter --template api
```

## Template Development Best Practices

### 1. Template Organization
- Keep templates focused on specific use cases
- Use clear, descriptive names and documentation
- Include comprehensive examples and documentation

### 2. Configuration Management
- Provide sensible defaults
- Use validation to catch configuration errors early
- Support environment variable overrides

### 3. Dependency Management
- Compute dependencies dynamically based on features
- Use optional dependencies for optional features
- Pin versions for stability

### 4. Testing
- Include comprehensive test suites in generated projects
- Test template generation with various configurations
- Validate generated projects can be built and run

### 5. Documentation
- Provide clear README files in generated projects
- Include configuration examples
- Document all available tools and resources

## Future Template Ideas

Potential templates that could be added:

- **API Gateway**: MCP server with REST API integration
- **Database Connector**: Direct database query and manipulation tools
- **File System**: File management and search capabilities
- **Cloud Services**: Integration with AWS, GCP, Azure services
- **Monitoring**: Observability and monitoring tools
- **Authentication**: Auth-enabled MCP servers
- **Workflow**: Process automation and workflow management
- **Analytics**: Data analysis and visualization tools
