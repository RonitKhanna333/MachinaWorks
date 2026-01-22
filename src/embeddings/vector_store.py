"""
Vector database manager using ChromaDB
Handles embedding creation and similarity search
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
import logging

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """Manages embeddings and retrieval using ChromaDB"""
    
    def __init__(
        self, 
        persist_directory: str = "data/vectordb",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize vector store
        
        Args:
            persist_directory: Directory to persist the database
            embedding_model: Sentence transformer model for embeddings
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )
        
        # Initialize embedding model
        logger.info(f"Loading HuggingFace embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        self.model_name = embedding_model
        
        # Create or get ChromaDB collection
        self.collection = self.client.get_or_create_collection(
            name="ai_use_cases",
            metadata={
                "description": "AI/ML/DL/RL use cases and solutions",
                "embedding_model": embedding_model,
                "vector_db": "ChromaDB"
            }
        )
        
        logger.info(f"✅ ChromaDB initialized with {self.collection.count()} documents")
        logger.info(f"✅ Using HuggingFace model: {embedding_model}")
    
    def embed_and_store(self, chunks_file: str = "data/processed/chunks.jsonl"):
        """Embed chunks and store in vector database"""
        
        chunks_path = Path(chunks_file)
        if not chunks_path.exists():
            raise FileNotFoundError(f"Chunks file not found: {chunks_file}")
        
        # Load chunks
        chunks = []
        with open(chunks_path, 'r', encoding='utf-8') as f:
            for line in f:
                chunks.append(json.loads(line))
        
        logger.info(f"Loaded {len(chunks)} chunks")
        
        # Prepare data for ChromaDB
        documents = [chunk['text'] for chunk in chunks]
        ids = [chunk['chunk_id'] for chunk in chunks]
        metadatas = []
        
        # Prepare metadata (ChromaDB only accepts str, int, float, bool, None)
        for chunk in chunks:
            metadata = chunk['metadata'].copy()
            metadata['chunk_type'] = chunk['chunk_type']
            
            # Convert lists to comma-separated strings
            for key, value in metadata.items():
                if isinstance(value, list):
                    metadata[key] = ', '.join(str(v) for v in value)
            
            metadatas.append(metadata)
        
        # Create embeddings using HuggingFace model
        logger.info(f"Creating embeddings with HuggingFace model: {self.model_name}...")
        embeddings = self.embedding_model.encode(
            documents, 
            show_progress_bar=True,
            convert_to_numpy=True,
            batch_size=32
        )
        
        # Store in ChromaDB (batch processing for large datasets)
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch_end = min(i + batch_size, len(chunks))
            
            self.collection.add(
                documents=documents[i:batch_end],
                embeddings=embeddings[i:batch_end].tolist(),
                ids=ids[i:batch_end],
                metadatas=metadatas[i:batch_end]
            )
            
            logger.info(f"Stored batch {i//batch_size + 1} ({batch_end}/{len(chunks)} chunks)")
        
        logger.info(f"✅ Stored {len(chunks)} chunks in vector database")
    
    def search(
        self, 
        query: str, 
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar use cases
        
        Args:
            query: User's problem description
            n_results: Number of results to return
            filter_dict: Optional metadata filters
        
        Returns:
            List of relevant use cases with metadata
        """
        # Create query embedding with HuggingFace model
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in ChromaDB using vector similarity
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_dict if filter_dict else None
        )
        
        # Format results
        formatted_results = []
        
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'chunk_id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def search_by_problem_type(self, problem: str, data_type: str = None) -> List[Dict]:
        """Search for use cases matching a specific problem and data type"""
        
        filter_dict = {}
        if data_type:
            filter_dict['data_type'] = {'$contains': data_type}
        
        return self.search(problem, n_results=5, filter_dict=filter_dict if filter_dict else None)
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector store"""
        count = self.collection.count()
        
        # Get sample to analyze metadata
        sample = self.collection.get(limit=min(count, 100))
        
        # Count chunk types
        chunk_types = {}
        data_types = {}
        
        for metadata in sample['metadatas']:
            chunk_type = metadata.get('chunk_type', 'unknown')
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
            
            data_type = metadata.get('data_type', 'unknown')
            if data_type:
                data_types[data_type] = data_types.get(data_type, 0) + 1
        
        return {
            'total_chunks': count,
            'chunk_types': chunk_types,
            'data_types': data_types
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Vector Store Manager')
    parser.add_argument(
        '--action',
        choices=['embed', 'search', 'stats'],
        default='embed',
        help='Action to perform'
    )
    parser.add_argument(
        '--query',
        type=str,
        help='Search query (for search action)'
    )
    
    args = parser.parse_args()
    
    # Initialize vector store
    vector_store = VectorStore()
    
    if args.action == 'embed':
        # Embed and store chunks
        vector_store.embed_and_store()
        
    elif args.action == 'search':
        if not args.query:
            print("Error: --query required for search action")
            return
        
        results = vector_store.search(args.query, n_results=3)
        
        print(f"\n{'='*60}")
        print(f"🔍 Search Results for: '{args.query}'")
        print(f"{'='*60}\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. Chunk ID: {result['chunk_id']}")
            print(f"   Distance: {result['distance']:.4f}")
            print(f"   Document: {result['document'][:200]}...")
            print(f"   Metadata: {result['metadata']}")
            print()
    
    elif args.action == 'stats':
        stats = vector_store.get_collection_stats()
        
        print(f"\n{'='*60}")
        print(f"📊 Vector Store Statistics")
        print(f"{'='*60}\n")
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"\nChunk types:")
        for chunk_type, count in stats['chunk_types'].items():
            print(f"  {chunk_type}: {count}")
        print(f"\nData types:")
        for data_type, count in stats['data_types'].items():
            print(f"  {data_type}: {count}")


if __name__ == '__main__':
    main()
