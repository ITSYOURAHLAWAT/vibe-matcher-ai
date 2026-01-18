from typing import TypedDict, List, Dict, Any, Optional

class GraphState(TypedDict):
    """
    Represents the state of the Vibe Matcher graph.
    """
    user_query: str
    
    # Analyst Output
    # We store the structured breakdown of the vibe
    analyst_thoughts: Optional[str] 
    refined_keywords: Optional[List[str]]
    
    # Retrieval Output
    retrieved_products: List[Dict[str, Any]]
    
    # Stylist Output
    stylist_pitch: Optional[str]
    
    # For error handling
    error: Optional[str]
