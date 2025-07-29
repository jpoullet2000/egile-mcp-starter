"""RAG (Retrieval-Augmented Generation) template plugin."""

from pathlib import Path
from typing import Any, Dict, List

from ..base import TemplatePlugin


class RAGTemplatePlugin(TemplatePlugin):
    """RAG MCP server template plugin with vector databases and retrieval
    capabilities."""

    def __init__(self) -> None:
        """Initialize the RAG template plugin."""
        super().__init__(
            name="rag",
            description=(
                "RAG-enabled MCP server with vector databases and retrieval tools"
            ),
            version="1.0.0",
        )

    def get_template_path(self) -> Path:
        """Get the path to the cookiecutter template directory.

        Returns:
            Path to the template directory containing cookiecutter.json
        """
        return Path(__file__).parent.parent.parent / "templates" / "rag"

    def get_default_context(self) -> Dict[str, Any]:
        """Get default context variables for the template.

        Returns:
            Dictionary of default template variables
        """
        return {
            "project_name": "My RAG MCP Server",
            "project_slug": "my_rag_mcp_server",
            "project_description": (
                "A RAG-enabled Model Context Protocol server "
                "with vector search capabilities"
            ),
            "author_name": "Your Name",
            "author_email": "your.email@example.com",
            "github_username": "yourusername",
            "version": "0.1.0",
            "python_version": "3.11",
            "use_docker": "y",
            "use_github_actions": "y",
            "use_pre_commit": "y",
            "license": "MIT",
            "include_examples": "y",
            "vector_db": "chroma",  # chroma, pinecone, weaviate, qdrant, faiss
            # sentence-transformers, openai, cohere
            "embedding_model": "sentence-transformers",
            "document_loaders": "y",  # Include various document loaders
            "web_scraping": "y",  # Include web scraping capabilities
            "pdf_processing": "y",  # Include PDF processing
            "chunk_strategy": "recursive",  # recursive, semantic, fixed
            "include_reranker": "y",  # Include reranking capabilities
        }

    def get_supported_features(self) -> List[str]:
        """Get list of features supported by this template.

        Returns:
            List of feature names
        """
        return [
            "docker",
            "github_actions",
            "pre_commit",
            "testing",
            "documentation",
            "multiple_licenses",
            "vector_databases",
            "embedding_models",
            "document_loaders",
            "web_scraping",
            "pdf_processing",
            "text_chunking",
            "semantic_search",
            "reranking",
            "examples",
        ]

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate the provided context for this template.

        Args:
            context: Template context variables

        Returns:
            True if context is valid, False otherwise
        """
        required_fields = ["project_name", "author_name", "author_email"]
        if not all(field in context and context[field] for field in required_fields):
            return False

        # Validate vector database choice
        valid_vector_dbs = ["chroma", "pinecone", "weaviate", "qdrant", "faiss"]
        if context.get("vector_db") not in valid_vector_dbs:
            return False

        # Validate embedding model choice
        valid_embedding_models = ["sentence-transformers", "openai", "cohere"]
        if context.get("embedding_model") not in valid_embedding_models:
            return False

        return True

    def pre_generate_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before project generation.

        Args:
            context: Template context variables

        Returns:
            Modified context variables
        """
        # Ensure project_slug is properly formatted based on project_name
        if "project_name" in context:
            project_slug = (
                context["project_name"].lower().replace(" ", "_").replace("-", "_")
            )
            context["project_slug"] = project_slug

        # Set up dependencies based on choices
        dependencies = ["fastmcp", "pydantic", "pyyaml", "click"]

        # Add specific dependencies
        dependencies.extend(self._get_vector_db_dependencies(context))
        dependencies.extend(self._get_embedding_dependencies(context))
        dependencies.extend(self._get_document_processing_dependencies(context))

        context["_computed_dependencies"] = dependencies
        return context

    def _get_vector_db_dependencies(self, context: Dict[str, Any]) -> list:
        """Get dependencies for the selected vector database."""
        vector_db = context.get("vector_db", "chroma")
        if vector_db == "chroma":
            return ["chromadb", "sqlite3"]
        elif vector_db == "pinecone":
            return ["pinecone-client"]
        elif vector_db == "weaviate":
            return ["weaviate-client"]
        elif vector_db == "qdrant":
            return ["qdrant-client"]
        elif vector_db == "faiss":
            return ["faiss-cpu", "numpy"]
        return []

    def _get_embedding_dependencies(self, context: Dict[str, Any]) -> list:
        """Get dependencies for the selected embedding model."""
        embedding_model = context.get("embedding_model", "sentence-transformers")
        if embedding_model == "sentence-transformers":
            return ["sentence-transformers"]
        elif embedding_model == "openai":
            return ["openai"]
        elif embedding_model == "cohere":
            return ["cohere"]
        return []

    def _get_document_processing_dependencies(self, context: Dict[str, Any]) -> list:
        """Get dependencies for document processing features."""
        deps = []

        if context.get("pdf_processing") == "y":
            deps.extend(["pypdf2", "pdfplumber"])

        if context.get("web_scraping") == "y":
            deps.extend(["requests", "beautifulsoup4", "scrapy"])

        if context.get("document_loaders") == "y":
            deps.extend(["python-docx", "openpyxl"])

        if context.get("include_reranker") == "y":
            deps.append("sentence-transformers")  # for cross-encoder models

        return deps

    def post_generate_hook(self, project_path: Path, context: Dict[str, Any]) -> None:
        """Hook called after project generation.

        Args:
            project_path: Path to the generated project
            context: Template context variables used during generation
        """
        # Could add RAG-specific post-generation steps like:
        # - Download default embedding models
        # - Initialize vector database
        # - Create sample documents for testing
        pass
