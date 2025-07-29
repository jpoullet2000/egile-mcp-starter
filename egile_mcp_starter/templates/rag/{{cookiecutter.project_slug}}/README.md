# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- 🔍 **Vector Search**: Powered by {{ cookiecutter.vector_db }}
- 🤖 **Embeddings**: Using {{ cookiecutter.embedding_model }}
- 📚 **Document Processing**: {% if cookiecutter.pdf_processing == 'y' %}PDF, {% endif %}{% if cookiecutter.document_loaders == 'y' %}DOCX, Excel, {% endif %}Text files
- 🌐 **Web Scraping**: {% if cookiecutter.web_scraping == 'y' %}Enabled{% else %}Disabled{% endif %}
- 🧠 **Chunking Strategy**: {{ cookiecutter.chunk_strategy }}
- 🔄 **Reranking**: {% if cookiecutter.include_reranker == 'y' %}Enabled{% else %}Disabled{% endif %}

## Installation

```bash
pip install -e .
```

## Configuration

Copy `config.example.yaml` to `config.yaml` and configure:

```yaml
vector_db:
  type: {{ cookiecutter.vector_db }}
  {% if cookiecutter.vector_db == 'chroma' %}
  path: "./data/chroma"
  {% elif cookiecutter.vector_db == 'pinecone' %}
  api_key: "your-pinecone-api-key"
  environment: "your-pinecone-environment"
  index_name: "your-index-name"
  {% elif cookiecutter.vector_db == 'weaviate' %}
  url: "http://localhost:8080"
  {% elif cookiecutter.vector_db == 'qdrant' %}
  url: "http://localhost:6333"
  {% endif %}

embedding:
  model: {{ cookiecutter.embedding_model }}
  {% if cookiecutter.embedding_model == 'openai' %}
  api_key: "your-openai-api-key"
  {% elif cookiecutter.embedding_model == 'cohere' %}
  api_key: "your-cohere-api-key"
  {% endif %}

chunking:
  strategy: {{ cookiecutter.chunk_strategy }}
  chunk_size: 1000
  chunk_overlap: 200

{% if cookiecutter.include_reranker == 'y' %}
reranker:
  model: "cross-encoder/ms-marco-MiniLM-L-6-v2"
  top_k: 10
{% endif %}
```

## Usage

### As MCP Server

Configure in your MCP client:

```json
{
  "mcpServers": {
    "{{ cookiecutter.project_slug }}": {
      "command": "python",
      "args": ["/path/to/{{ cookiecutter.project_slug }}/src/main.py"],
      "env": {
        "LOG_LEVEL": "INFO",
        "CONFIG_PATH": "/path/to/config.yaml"
      }
    }
  }
}
```

### Available Tools

- `ingest_documents`: Add documents to the vector database
- `search_documents`: Semantic search across indexed documents
- `get_document_chunks`: Retrieve specific document chunks
{% if cookiecutter.web_scraping == 'y' %}
- `scrape_and_index`: Scrape web pages and add to index
{% endif %}
{% if cookiecutter.include_reranker == 'y' %}
- `rerank_results`: Rerank search results for better relevance
{% endif %}

### Available Resources

- `documents://list`: List all indexed documents
- `documents://metadata/{doc_id}`: Get document metadata
- `chunks://search?q={query}`: Search document chunks

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Type checking
mypy src/
```

## License

This project is licensed under the {{ cookiecutter.license }} License.

---

Built with ❤️ using [FASTMCP](https://github.com/jlowin/fastmcp) and the [Model Context Protocol](https://modelcontextprotocol.io/)
