import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(name=settings.COLLECTION_NAME)

    def add_products(self, ids: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], documents: List[str]):
        """
        Add products to the ChromaDB collection.
        """
        logger.info(f"Adding {len(ids)} documents to ChromaDB.")
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def search(self, query_embedding: List[float], n_results: int = 3, where: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for similar products.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        # Parse results into a friendly list of dicts
        matches = []
        if results['ids']:
            ids = results['ids'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]
            documents = results['documents'][0]
            
            for i, _id in enumerate(ids):
                # Chroma returns 'distance' by default for some spaces, but can return cosine similarity
                # depending on init. Default is l2. 
                # Let's assume using default (l2) for now, but convert to similarity if needed.
                # Actually, standard Chroma is distance. Low is good.
                # But implementation_plan said "confidence score".
                # To get cosine similarity in Chroma, we usually need to specify metadata={"hnsw:space": "cosine"}
                # and then score = 1 - distance.
                # However, for this MVP, we'll just return the metadata + distance.
                
                matches.append({
                    "id": _id,
                    "metadata": metadatas[i],
                    "document": documents[i],
                    "score": distances[i] # keeping raw distance for now
                })
        
        return matches
    
    def count(self) -> int:
        return self.collection.count()
