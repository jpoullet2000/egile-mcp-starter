"""Configuration management for RAG MCP server."""

from typing import Any, Dict, Optional
from pydantic import BaseModel


class EmbeddingConfig(BaseModel):
    """Configuration for embedding models."""
    model: str
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    device: str = "cpu"


class VectorDBConfig(BaseModel):
    """Configuration for vector database."""
    type: str
    path: Optional[str] = None
    collection_name: str = "documents"
    api_key: Optional[str] = None
    environment: Optional[str] = None
    index_name: Optional[str] = None
    url: Optional[str] = None
    class_name: Optional[str] = None


class ChunkingConfig(BaseModel):
    """Configuration for text chunking."""
    strategy: str = "recursive"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    similarity_threshold: Optional[float] = None
    separators: Optional[list] = None


{% if cookiecutter.include_reranker == 'y' %}
class RerankerConfig(BaseModel):
    """Configuration for reranking."""
    enabled: bool = True
    model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_k: int = 10
    score_threshold: float = 0.3
{% endif %}


{% if cookiecutter.web_scraping == 'y' %}
class WebScrapingConfig(BaseModel):
    """Configuration for web scraping."""
    user_agent: str = "{{ cookiecutter.project_slug }}/{{ cookiecutter.version }}"
    max_pages: int = 100
    delay: float = 1.0
    timeout: int = 30
{% endif %}


{% if cookiecutter.pdf_processing == 'y' %}
class PDFProcessingConfig(BaseModel):
    """Configuration for PDF processing."""
    extract_images: bool = False
    preserve_layout: bool = True
    password: Optional[str] = None
{% endif %}


class DocumentProcessingConfig(BaseModel):
    """Configuration for document processing."""
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: list = [".txt", ".md", ".rst"]
    ignore_patterns: list = ["*.tmp", "*.log", "__pycache__/*"]


class SearchConfig(BaseModel):
    """Configuration for search functionality."""
    default_limit: int = 10
    max_limit: int = 100
    similarity_threshold: float = 0.7
    {% if cookiecutter.include_reranker == 'y' %}
    use_reranking: bool = True
    {% endif %}


class CacheConfig(BaseModel):
    """Configuration for caching."""
    enabled: bool = True
    ttl: int = 3600  # 1 hour
    max_size: int = 1000


class ServerConfig(BaseModel):
    """Configuration for the server."""
    host: str = "localhost"
    port: int = 8000
    log_level: str = "INFO"


class RAGConfig(BaseModel):
    """Main configuration for RAG MCP server."""
    server: ServerConfig
    vector_db: VectorDBConfig
    embedding: EmbeddingConfig
    chunking: ChunkingConfig
    {% if cookiecutter.include_reranker == 'y' %}
    reranker: RerankerConfig
    {% endif %}
    {% if cookiecutter.web_scraping == 'y' %}
    web_scraping: WebScrapingConfig
    {% endif %}
    {% if cookiecutter.pdf_processing == 'y' %}
    pdf_processing: PDFProcessingConfig
    {% endif %}
    document_processing: DocumentProcessingConfig
    search: SearchConfig
    cache: CacheConfig
