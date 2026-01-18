from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    desc: str
    vibes: List[str]
    
    # Metadata for filtering/retrieval
    # We might flatten vibes into a string for embedding text, 
    # but keep them structured for metadata.

class MatchRequest(BaseModel):
    query: str
    
class MatchResponse(BaseModel):
    matches: List[Dict[str, Any]]
    analyst_insights: Optional[Dict[str, Any]] = None
    stylist_pitch: Optional[str] = None
