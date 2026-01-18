import json
import logging
from typing import Dict, Any, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.core.config import settings
from app.services.workflow.state import GraphState
from app.services.vector_store import VectorStore
from app.services.embedding import EmbeddingService

logger = logging.getLogger(__name__)

# Initialize singletons for efficiency
_llm = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY, temperature=0.7)
_vector_store = VectorStore()
_embedding_service = EmbeddingService()

# --- Vibe Analyst Node ---

async def vibe_analyst_node(state: GraphState) -> Dict[str, Any]:
    """
    Vibe Analyst Agent: Break down the user's vague query.
    Uses Chain-of-Thought to extract attributes.
    """
    logger.info("--- Node: Vibe Analyst ---")
    query = state["user_query"]
    
    # Chain of thought prompt
    system_prompt = """You are an expert Fashion Vibe Analyst. 
    Your goal is to deconstruct a user's vague fashion request into concrete, searchable attributes.
    
    Follow this Chain-of-Thought process:
    1. ANALYZE: What is the core "vibe" or aesthetic? (e.g., Cyberpunk, Boho, Minimalist)
    2. KEYWORDS: specific visual elements, fabrics, colors, or item types.
    3. SEARCH TERMS: A list of 3-5 concise search strings that would work well in a vector database.
    
    Respond in JSON format:
    {
        "thought_process": "Analysis description...",
        "search_terms": ["term1", "term2", "term3"]
    }
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{query}")
    ])
    
    chain = prompt | _llm | JsonOutputParser()
    
    try:
        # Use ainvoke for async
        result = await chain.ainvoke({"query": query})
        return {
            "analyst_thoughts": result.get("thought_process", ""),
            "refined_keywords": result.get("search_terms", [])
        }
    except Exception as e:
        logger.error(f"Vibe Analyst failed: {e}")
        return {
            "analyst_thoughts": "Failed to analyze, using raw query.",
            "refined_keywords": [query]
        }

# --- Retriever Node ---

def retriever_node(state: GraphState) -> Dict[str, Any]:
    """
    Retriever Node: Embeds search terms and queries ChromaDB.
    """
    logger.info("--- Node: Retriever ---")
    keywords = state.get("refined_keywords", [])
    if not keywords:
        keywords = [state["user_query"]]
        
    # Combine keywords into a single rich query for embedding
    combined_query = " ".join(keywords)
    
    # Generate embedding
    query_embedding = _embedding_service.embed_text(combined_query)
    
    # Search
    results = _vector_store.search(query_embedding=query_embedding, n_results=3)
    
    return {"retrieved_products": results}

# --- Stylist Node ---

async def stylist_node(state: GraphState) -> Dict[str, Any]:
    """
    Stylist Agent: Generate a personalized sales pitch.
    """
    logger.info("--- Node: Stylist ---")
    user_query = state["user_query"]
    products = state.get("retrieved_products", [])
    analyst_thoughts = state.get("analyst_thoughts", "")
    
    if not products:
        return {"stylist_pitch": "I couldn't find any items that match your specific vibe perfectly, but I'm always looking for new styles!"}
    
    # Format products for the prompt
    products_str = ""
    for idx, p in enumerate(products):
        meta = p.get("metadata", {})
        products_str += f"{idx+1}. {meta.get('name', 'Unknown')}: {meta.get('desc', 'No desc')} (Vibes: {meta.get('vibes', '')})\n"
        
    system_prompt = """You are an elite Personal Stylist. 
    The user asked for: "{user_query}"
    
    Our Vibe Analyst noted: "{analyst_thoughts}"
    
    We found these matching items:
    {products_str}
    
    Your task:
    Write a short, engaging, and personalized sales pitch explaining WHY these specific items fit the user's requested vibe.
    Be enthusiastic but professional. Focus on the *vibe* match.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Write the pitch.")
    ])
    
    chain = prompt | _llm | StrOutputParser()
    
    # Use ainvoke for async
    response = await chain.ainvoke({
        "user_query": user_query,
        "analyst_thoughts": analyst_thoughts,
        "products_str": products_str
    })
    
    return {"stylist_pitch": response}
