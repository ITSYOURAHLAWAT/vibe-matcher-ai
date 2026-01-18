import uuid
import logging
from typing import List, Dict
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStore
from app.models.domain import Product

logger = logging.getLogger(__name__)

MOCK_PRODUCTS = [
    {
        "name": "Boho Breeze Dress",
        "desc": "Flowy midi dress with earthy tones, tassels, and relaxed silhouette—perfect for festivals and beach sunsets.",
        "vibes": ["boho", "free-spirited", "summer"]
    },
    {
        "name": "Urban Sprint Sneakers",
        "desc": "Lightweight streetwear sneakers with bold accents and responsive sole, built for energetic city walks.",
        "vibes": ["urban", "energetic", "athleisure"]
    },
    {
        "name": "Cozy Cloud Hoodie",
        "desc": "Ultra-soft oversized hoodie in heather gray with fleece lining for stay-at-home cozy winter evenings.",
        "vibes": ["cozy", "casual", "winter"]
    },
    {
        "name": "Minimalist Monochrome Blazer",
        "desc": "Clean, sharp lines in a matte black blazer—minimalist, office-friendly, and capsule-wardrobe essential.",
        "vibes": ["minimalist", "monochrome", "office"]
    },
    {
        "name": "Vintage Indigo Denim Jacket",
        "desc": "Boxy-fit denim jacket with subtle distressing and classic metal hardware for timeless street style.",
        "vibes": ["vintage", "street", "casual"]
    },
    {
        "name": "Pastel Pop Skirt",
        "desc": "Pleated A-line skirt in pastel palette with playful movement and soft satin sheen.",
        "vibes": ["playful", "pastel", "feminine"]
    },
    {
        "name": "Trail Tech Windbreaker",
        "desc": "Water-resistant windbreaker with breathable mesh panels—ideal for hikes, drizzles, and weekend getaways.",
        "vibes": ["outdoor", "techwear", "utility"]
    },
    {
        "name": "Silk Evening Top",
        "desc": "Sleek silk cami with delicate straps and subtle sheen—goes from dinner dates to cocktails effortlessly.",
        "vibes": ["elegant", "evening", "chic"]
    },
    {
        "name": "Retro Court Sneakers",
        "desc": "Low-top leather sneakers with gum sole and retro side stripes for heritage tennis aesthetics.",
        "vibes": ["retro", "sporty", "street"]
    },
    {
        "name": "Ribbed Knit Co-ord",
        "desc": "Two-piece ribbed knit set with stretch comfort—balanced lines for lounge-to-errand versatility.",
        "vibes": ["loungewear", "neutral", "minimal"]
    },
]

class IngestionPipeline:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def run(self):
        """
        Runs the ingestion pipeline:
        1. Check if data exists.
        2. If not, load mock data.
        3. Embed.
        4. Store.
        """
        count = self.vector_store.count()
        if count > 0:
            logger.info(f"Vector store already contains {count} items. Skipping ingestion.")
            return

        logger.info("Starting ingestion pipeline...")
        
        products = []
        texts = []
        ids = []
        metadatas = []
        
        for p in MOCK_PRODUCTS:
            # Create a rich text representation for embedding
            # "Name: ... Desc: ... Vibes: ..."
            text_rep = f"Name: {p['name']}. Description: {p['desc']}. Vibes: {', '.join(p['vibes'])}"
            
            _id = str(uuid.uuid4())
            
            products.append(p)
            texts.append(text_rep)
            ids.append(_id)
            metadatas.append({
                "name": p["name"],
                "desc": p["desc"],
                # Chroma metadata must be flat primitives
                "vibes": ", ".join(p["vibes"])
            })

        logger.info(f"Generating embeddings for {len(texts)} products...")
        embeddings = self.embedding_service.embed_texts(texts)
        
        logger.info("Storing in VectorDB...")
        self.vector_store.add_products(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts
        )
        
        logger.info("Ingestion complete.")

if __name__ == "__main__":
    # Helper to run manually
    import sys
    # Include project root in path if run as script
    sys.path.append(".") 
    from app.core.logging import setup_logging
    setup_logging()
    
    pipeline = IngestionPipeline()
    pipeline.run()
