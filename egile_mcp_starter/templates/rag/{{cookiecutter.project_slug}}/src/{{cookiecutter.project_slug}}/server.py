"""RAG MCP server implementation."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from fastmcp import FastMCP

from .config import RAGConfig
from .embeddings import EmbeddingManager
from .vector_store import VectorStoreManager
from .document_processor import DocumentProcessor
{% if cookiecutter.include_reranker == 'y' %}
from .reranker import RerankerManager
{% endif %}


logger = logging.getLogger(__name__)


def create_rag_server(config_path: str) -> FastMCP:
    """Create a RAG MCP server instance.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        FastMCP server instance
    """
    # Load configuration
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    config = RAGConfig(**config_dict)
    
    # Initialize components
    embedding_manager = EmbeddingManager(config.embedding)
    vector_store = VectorStoreManager(config.vector_db)
    document_processor = DocumentProcessor(config.document_processing, config.chunking)
    {% if cookiecutter.include_reranker == 'y' %}
    reranker = RerankerManager(config.reranker) if config.reranker.enabled else None
    {% endif %}
    
    # Create FastMCP server
    server = FastMCP("{{ cookiecutter.project_name }}")
    
    @server.tool("ingest_documents")
    async def ingest_documents(
        documents: List[str], 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Ingest documents into the vector database.
        
        Args:
            documents: List of document paths or URLs to ingest
            metadata: Optional metadata to associate with documents
            
        Returns:
            Result of the ingestion process
        """
        try:
            results = []
            for doc_path in documents:
                # Process document
                chunks = await document_processor.process_document(doc_path)
                
                # Generate embeddings
                embeddings = await embedding_manager.embed_texts([chunk.text for chunk in chunks])
                
                # Store in vector database
                doc_metadata = metadata or {}
                doc_metadata['source'] = doc_path
                
                chunk_ids = await vector_store.add_chunks(
                    texts=[chunk.text for chunk in chunks],
                    embeddings=embeddings,
                    metadata=[{**doc_metadata, **chunk.metadata} for chunk in chunks]
                )
                
                results.append({
                    'document': doc_path,
                    'chunks_added': len(chunk_ids),
                    'chunk_ids': chunk_ids
                })
            
            return {
                'status': 'success',
                'documents_processed': len(results),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error ingesting documents: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @server.tool("search_documents")
    async def search_documents(
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.7,
        {% if cookiecutter.include_reranker == 'y' %}
        use_reranking: bool = True
        {% endif %}
    ) -> Dict[str, Any]:
        """Search for relevant documents using semantic similarity.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score for results
            {% if cookiecutter.include_reranker == 'y' %}
            use_reranking: Whether to apply reranking to improve results
            {% endif %}
            
        Returns:
            Search results with relevance scores
        """
        try:
            # Generate query embedding
            query_embedding = await embedding_manager.embed_text(query)
            
            # Search vector database
            search_limit = limit
            {% if cookiecutter.include_reranker == 'y' %}
            if use_reranking and reranker:
                search_limit = min(limit * 3, 50)  # Get more results for reranking
            {% endif %}
            
            results = await vector_store.search(
                query_embedding=query_embedding,
                limit=search_limit,
                similarity_threshold=similarity_threshold
            )
            
            {% if cookiecutter.include_reranker == 'y' %}
            # Apply reranking if enabled
            if use_reranking and reranker and results:
                results = await reranker.rerank(query, results, limit)
            {% endif %}
            
            return {
                'status': 'success',
                'query': query,
                'results_count': len(results),
                'results': [
                    {
                        'text': result.text,
                        'score': result.score,
                        'metadata': result.metadata
                    }
                    for result in results[:limit]
                ]
            }
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @server.tool("get_document_chunks")
    async def get_document_chunks(
        document_id: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get chunks from a specific document.
        
        Args:
            document_id: ID of the document
            limit: Maximum number of chunks to return
            
        Returns:
            Document chunks
        """
        try:
            chunks = await vector_store.get_document_chunks(document_id, limit)
            
            return {
                'status': 'success',
                'document_id': document_id,
                'chunks_count': len(chunks),
                'chunks': [
                    {
                        'text': chunk.text,
                        'metadata': chunk.metadata
                    }
                    for chunk in chunks
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting document chunks: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    {% if cookiecutter.web_scraping == 'y' %}
    @server.tool("scrape_and_index")
    async def scrape_and_index(
        urls: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Scrape web pages and add them to the index.
        
        Args:
            urls: List of URLs to scrape and index
            metadata: Optional metadata to associate with scraped content
            
        Returns:
            Result of the scraping and indexing process
        """
        try:
            from .web_scraper import WebScraper
            
            scraper = WebScraper(config.web_scraping)
            results = []
            
            for url in urls:
                # Scrape content
                content = await scraper.scrape_url(url)
                
                if content:
                    # Process as document
                    chunks = await document_processor.process_text(content, {'source_url': url})
                    
                    # Generate embeddings
                    embeddings = await embedding_manager.embed_texts([chunk.text for chunk in chunks])
                    
                    # Store in vector database
                    doc_metadata = metadata or {}
                    doc_metadata.update({'source': url, 'type': 'web_page'})
                    
                    chunk_ids = await vector_store.add_chunks(
                        texts=[chunk.text for chunk in chunks],
                        embeddings=embeddings,
                        metadata=[{**doc_metadata, **chunk.metadata} for chunk in chunks]
                    )
                    
                    results.append({
                        'url': url,
                        'chunks_added': len(chunk_ids),
                        'chunk_ids': chunk_ids
                    })
                else:
                    results.append({
                        'url': url,
                        'error': 'Failed to scrape content'
                    })
            
            return {
                'status': 'success',
                'urls_processed': len(results),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error scraping and indexing: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    {% endif %}
    
    # Resources
    @server.resource("documents://list")
    async def list_documents() -> str:
        """List all indexed documents."""
        try:
            documents = await vector_store.list_documents()
            return "\n".join([f"- {doc['id']}: {doc['metadata'].get('source', 'Unknown')}" for doc in documents])
        except Exception as e:
            return f"Error listing documents: {e}"
    
    @server.resource("documents://metadata/{doc_id}")
    async def get_document_metadata(doc_id: str) -> str:
        """Get metadata for a specific document."""
        try:
            metadata = await vector_store.get_document_metadata(doc_id)
            if metadata:
                return yaml.dump(metadata, default_flow_style=False)
            else:
                return f"Document {doc_id} not found"
        except Exception as e:
            return f"Error getting document metadata: {e}"
    
    @server.resource("chunks://search")
    async def search_chunks(q: str) -> str:
        """Search document chunks and return as formatted text."""
        try:
            result = await search_documents(q, limit=5)
            if result['status'] == 'success':
                chunks = []
                for item in result['results']:
                    chunks.append(f"Score: {item['score']:.3f}")
                    chunks.append(f"Source: {item['metadata'].get('source', 'Unknown')}")
                    chunks.append(f"Text: {item['text'][:200]}...")
                    chunks.append("---")
                return "\n".join(chunks)
            else:
                return f"Search error: {result['message']}"
        except Exception as e:
            return f"Error searching chunks: {e}"
    
    return server
