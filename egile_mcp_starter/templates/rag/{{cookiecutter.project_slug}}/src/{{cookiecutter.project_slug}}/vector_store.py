"""Vector store implementation for different vector databases."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from pydantic import BaseModel

from .config import VectorDBConfig

logger = logging.getLogger(__name__)


class SearchResult(BaseModel):
    """Search result from vector store."""
    
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}


class VectorStore(ABC):
    """Abstract base class for vector stores."""
    
    @abstractmethod
    async def add_chunks(
        self, 
        chunks: List[Dict[str, Any]], 
        embeddings: List[List[float]]
    ) -> List[str]:
        """Add chunks with embeddings to the vector store.
        
        Args:
            chunks: List of chunk data with metadata
            embeddings: List of embedding vectors
            
        Returns:
            List of chunk IDs
        """
        pass
    
    @abstractmethod
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search for similar chunks.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of search results
        """
        pass
    
    @abstractmethod
    async def get_document_chunks(
        self, 
        document_id: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all chunks for a document.
        
        Args:
            document_id: Document identifier
            limit: Optional limit on number of chunks
            
        Returns:
            List of chunk data
        """
        pass
    
    @abstractmethod
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in the store.
        
        Returns:
            List of document metadata
        """
        pass
    
    @abstractmethod
    async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
        """Get metadata for a document.
        
        Args:
            document_id: Document identifier
            
        Returns:
            Document metadata
        """
        pass


{% if cookiecutter.vector_db == 'chroma' %}
class ChromaVectorStore(VectorStore):
    """ChromaDB vector store implementation."""
    
    def __init__(self, config: VectorDBConfig):
        """Initialize ChromaDB vector store."""
        import chromadb
        from chromadb.config import Settings
        
        self.config = config
        self.client = chromadb.PersistentClient(
            path=config.database_url or "./chroma_db",
            settings=Settings(allow_reset=True)
        )
        self.collection = self.client.get_or_create_collection(
            name=config.collection_name or "documents"
        )
    
    async def add_chunks(
        self, 
        chunks: List[Dict[str, Any]], 
        embeddings: List[List[float]]
    ) -> List[str]:
        """Add chunks to ChromaDB."""
        chunk_ids = [chunk['id'] for chunk in chunks]
        documents = [chunk['content'] for chunk in chunks]
        metadatas = [chunk.get('metadata', {}) for chunk in chunks]
        
        self.collection.add(
            ids=chunk_ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        return chunk_ids
    
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search ChromaDB for similar chunks."""
        where = filters if filters else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )
        
        search_results = []
        for i in range(len(results['ids'][0])):
            search_results.append(SearchResult(
                chunk_id=results['ids'][0][i],
                document_id=results['metadatas'][0][i].get('document_id', ''),
                content=results['documents'][0][i],
                score=1.0 - results['distances'][0][i],  # Convert distance to similarity
                metadata=results['metadatas'][0][i]
            ))
        
        return search_results
    
    async def get_document_chunks(
        self, 
        document_id: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get chunks for a document from ChromaDB."""
        results = self.collection.get(
            where={"document_id": document_id},
            limit=limit
        )
        
        chunks = []
        for i in range(len(results['ids'])):
            chunks.append({
                'id': results['ids'][i],
                'content': results['documents'][i],
                'metadata': results['metadatas'][i]
            })
        
        return chunks
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in ChromaDB."""
        # ChromaDB doesn't have direct document listing, so we aggregate from chunks
        results = self.collection.get()
        document_ids = set()
        
        for metadata in results['metadatas']:
            if 'document_id' in metadata:
                document_ids.add(metadata['document_id'])
        
        return [{'id': doc_id} for doc_id in document_ids]
    
    async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
        """Get document metadata from ChromaDB."""
        results = self.collection.get(
            where={"document_id": document_id},
            limit=1
        )
        
        if results['metadatas']:
            return results['metadatas'][0]
        return {}


{% elif cookiecutter.vector_db == 'faiss' %}
class FAISSVectorStore(VectorStore):
    """FAISS vector store implementation."""
    
    def __init__(self, config: VectorDBConfig):
        """Initialize FAISS vector store."""
        import faiss
        import pickle
        
        self.config = config
        self.index_path = Path(config.database_url or "./faiss_index")
        self.index_path.mkdir(exist_ok=True)
        
        self.index_file = self.index_path / "index.faiss"
        self.metadata_file = self.index_path / "metadata.pkl"
        
        # Initialize or load index
        self.dimension = config.dimension or 384  # Default for sentence-transformers
        self.index = None
        self.metadata_store = {}
        self.chunk_counter = 0
        
        self._load_index()
    
    def _load_index(self):
        """Load existing index or create new one."""
        import faiss
        import pickle
        
        if self.index_file.exists() and self.metadata_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            with open(self.metadata_file, 'rb') as f:
                self.metadata_store = pickle.load(f)
            self.chunk_counter = len(self.metadata_store)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)  # Inner product (cosine similarity)
            self.metadata_store = {}
            self.chunk_counter = 0
    
    def _save_index(self):
        """Save index and metadata to disk."""
        import faiss
        import pickle
        
        faiss.write_index(self.index, str(self.index_file))
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(self.metadata_store, f)
    
    async def add_chunks(
        self, 
        chunks: List[Dict[str, Any]], 
        embeddings: List[List[float]]
    ) -> List[str]:
        """Add chunks to FAISS index."""
        import numpy as np
        
        # Normalize embeddings for cosine similarity
        embeddings_array = np.array(embeddings, dtype=np.float32)
        embeddings_array = embeddings_array / np.linalg.norm(embeddings_array, axis=1, keepdims=True)
        
        # Add to index
        self.index.add(embeddings_array)
        
        # Store metadata
        chunk_ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = chunk.get('id', f"chunk_{self.chunk_counter}")
            chunk_ids.append(chunk_id)
            
            self.metadata_store[self.chunk_counter] = {
                'chunk_id': chunk_id,
                'document_id': chunk.get('document_id', ''),
                'content': chunk.get('content', ''),
                'metadata': chunk.get('metadata', {})
            }
            self.chunk_counter += 1
        
        self._save_index()
        return chunk_ids
    
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search FAISS index for similar chunks."""
        import numpy as np
        
        if self.index.ntotal == 0:
            return []
        
        # Normalize query embedding
        query_array = np.array([query_embedding], dtype=np.float32)
        query_array = query_array / np.linalg.norm(query_array, axis=1, keepdims=True)
        
        # Search
        scores, indices = self.index.search(query_array, min(top_k, self.index.ntotal))
        
        search_results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx == -1:  # Invalid result
                continue
                
            metadata_entry = self.metadata_store.get(idx, {})
            
            # Apply filters if provided
            if filters:
                match = True
                for key, value in filters.items():
                    if metadata_entry.get('metadata', {}).get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            search_results.append(SearchResult(
                chunk_id=metadata_entry.get('chunk_id', f'chunk_{idx}'),
                document_id=metadata_entry.get('document_id', ''),
                content=metadata_entry.get('content', ''),
                score=float(score),
                metadata=metadata_entry.get('metadata', {})
            ))
        
        return search_results
    
    async def get_document_chunks(
        self, 
        document_id: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get chunks for a document from FAISS store."""
        chunks = []
        count = 0
        
        for idx, metadata_entry in self.metadata_store.items():
            if metadata_entry.get('document_id') == document_id:
                chunks.append({
                    'id': metadata_entry.get('chunk_id'),
                    'content': metadata_entry.get('content'),
                    'metadata': metadata_entry.get('metadata', {})
                })
                count += 1
                
                if limit and count >= limit:
                    break
        
        return chunks
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in FAISS store."""
        document_ids = set()
        
        for metadata_entry in self.metadata_store.values():
            doc_id = metadata_entry.get('document_id')
            if doc_id:
                document_ids.add(doc_id)
        
        return [{'id': doc_id} for doc_id in document_ids]
    
    async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
        """Get document metadata from FAISS store."""
        for metadata_entry in self.metadata_store.values():
            if metadata_entry.get('document_id') == document_id:
                return metadata_entry.get('metadata', {})
        
        return {}


{% elif cookiecutter.vector_db == 'pinecone' %}
class PineconeVectorStore(VectorStore):
    """Pinecone vector store implementation."""
    
    def __init__(self, config: VectorDBConfig):
        """Initialize Pinecone vector store."""
        import pinecone
        
        self.config = config
        
        # Initialize Pinecone
        pinecone.init(
            api_key=config.api_key,
            environment=config.environment or 'us-west1-gcp'
        )
        
        self.index_name = config.index_name or 'documents'
        
        # Create index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=config.dimension or 384,
                metric='cosine'
            )
        
        self.index = pinecone.Index(self.index_name)
    
    async def add_chunks(
        self, 
        chunks: List[Dict[str, Any]], 
        embeddings: List[List[float]]
    ) -> List[str]:
        """Add chunks to Pinecone."""
        vectors = []
        chunk_ids = []
        
        for chunk, embedding in zip(chunks, embeddings):
            chunk_id = chunk.get('id', f"chunk_{len(chunk_ids)}")
            chunk_ids.append(chunk_id)
            
            metadata = chunk.get('metadata', {})
            metadata.update({
                'document_id': chunk.get('document_id', ''),
                'content': chunk.get('content', '')
            })
            
            vectors.append({
                'id': chunk_id,
                'values': embedding,
                'metadata': metadata
            })
        
        self.index.upsert(vectors)
        return chunk_ids
    
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search Pinecone for similar chunks."""
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            filter=filters,
            include_metadata=True
        )
        
        search_results = []
        for match in results['matches']:
            metadata = match.get('metadata', {})
            search_results.append(SearchResult(
                chunk_id=match['id'],
                document_id=metadata.get('document_id', ''),
                content=metadata.get('content', ''),
                score=match['score'],
                metadata={k: v for k, v in metadata.items() 
                         if k not in ['document_id', 'content']}
            ))
        
        return search_results
    
    async def get_document_chunks(
        self, 
        document_id: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get chunks for a document from Pinecone."""
        # Pinecone doesn't support direct filtering in fetch, so we use query
        dummy_vector = [0.0] * (self.config.dimension or 384)
        
        results = self.index.query(
            vector=dummy_vector,
            top_k=limit or 10000,  # Large number to get all
            filter={'document_id': document_id},
            include_metadata=True
        )
        
        chunks = []
        for match in results['matches']:
            metadata = match.get('metadata', {})
            chunks.append({
                'id': match['id'],
                'content': metadata.get('content', ''),
                'metadata': {k: v for k, v in metadata.items() 
                           if k not in ['document_id', 'content']}
            })
        
        return chunks
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in Pinecone."""
        # This is a limitation of Pinecone - we can't easily list all unique document_ids
        # This would require maintaining a separate index or using describe_index_stats
        stats = self.index.describe_index_stats()
        return [{'note': 'Document listing not fully supported by Pinecone'}]
    
    async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
        """Get document metadata from Pinecone."""
        # Similar limitation - we'd need to store document metadata separately
        # or query for any chunk from the document
        dummy_vector = [0.0] * (self.config.dimension or 384)
        
        results = self.index.query(
            vector=dummy_vector,
            top_k=1,
            filter={'document_id': document_id},
            include_metadata=True
        )
        
        if results['matches']:
            return results['matches'][0].get('metadata', {})
        return {}


{% else %}
# Default/fallback implementation for other vector stores
class DefaultVectorStore(VectorStore):
    """Default in-memory vector store implementation."""
    
    def __init__(self, config: VectorDBConfig):
        """Initialize default vector store."""
        self.config = config
        self.chunks = []
        self.embeddings = []
    
    async def add_chunks(
        self, 
        chunks: List[Dict[str, Any]], 
        embeddings: List[List[float]]
    ) -> List[str]:
        """Add chunks to in-memory store."""
        chunk_ids = []
        for chunk, embedding in zip(chunks, embeddings):
            chunk_id = chunk.get('id', f"chunk_{len(self.chunks)}")
            chunk_ids.append(chunk_id)
            
            self.chunks.append({
                'id': chunk_id,
                'document_id': chunk.get('document_id', ''),
                'content': chunk.get('content', ''),
                'metadata': chunk.get('metadata', {})
            })
            self.embeddings.append(embedding)
        
        return chunk_ids
    
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search in-memory store for similar chunks."""
        import numpy as np
        
        if not self.embeddings:
            return []
        
        # Calculate cosine similarities
        query_array = np.array(query_embedding)
        embeddings_array = np.array(self.embeddings)
        
        # Normalize vectors
        query_norm = query_array / np.linalg.norm(query_array)
        embeddings_norm = embeddings_array / np.linalg.norm(embeddings_array, axis=1, keepdims=True)
        
        # Calculate similarities
        similarities = np.dot(embeddings_norm, query_norm)
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        search_results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            
            # Apply filters if provided
            if filters:
                match = True
                for key, value in filters.items():
                    if chunk.get('metadata', {}).get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            search_results.append(SearchResult(
                chunk_id=chunk['id'],
                document_id=chunk['document_id'],
                content=chunk['content'],
                score=float(similarities[idx]),
                metadata=chunk.get('metadata', {})
            ))
        
        return search_results
    
    async def get_document_chunks(
        self, 
        document_id: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get chunks for a document from in-memory store."""
        chunks = [chunk for chunk in self.chunks if chunk['document_id'] == document_id]
        
        if limit:
            chunks = chunks[:limit]
        
        return chunks
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in in-memory store."""
        document_ids = set(chunk['document_id'] for chunk in self.chunks if chunk['document_id'])
        return [{'id': doc_id} for doc_id in document_ids]
    
    async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
        """Get document metadata from in-memory store."""
        for chunk in self.chunks:
            if chunk['document_id'] == document_id:
                return chunk.get('metadata', {})
        return {}

{% endif %}


class VectorStoreManager:
    """Manager for vector store operations."""
    
    def __init__(self, config: VectorDBConfig):
        """Initialize vector store manager.
        
        Args:
            config: Vector database configuration
        """
        self.config = config
        
        # Initialize the appropriate vector store
        {% if cookiecutter.vector_db == 'chroma' %}
        self.store = ChromaVectorStore(config)
        {% elif cookiecutter.vector_db == 'faiss' %}
        self.store = FAISSVectorStore(config)
        {% elif cookiecutter.vector_db == 'pinecone' %}
        self.store = PineconeVectorStore(config)
        {% else %}
        self.store = DefaultVectorStore(config)
        {% endif %}
    
    async def add_chunks(
        self, 
        chunks: List[Dict[str, Any]], 
        embeddings: List[List[float]]
    ) -> List[str]:
        """Add chunks with embeddings to the vector store."""
        return await self.store.add_chunks(chunks, embeddings)
    
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search for similar chunks."""
        return await self.store.search(query_embedding, top_k, filters)
    
    async def get_document_chunks(
        self, 
        document_id: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all chunks for a document."""
        return await self.store.get_document_chunks(document_id, limit)
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in the store."""
        return await self.store.list_documents()
    
    async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
        """Get metadata for a document."""
        return await self.store.get_document_metadata(document_id)
