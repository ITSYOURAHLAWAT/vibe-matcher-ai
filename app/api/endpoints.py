import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.domain import MatchRequest
from app.services.workflow.graph import vibe_graph
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat")
async def chat(request: MatchRequest):
    """
    Streaming chat endpoint that runs the Vibe Matcher LangGraph.
    Returns a stream of JSON events.
    """
    
    async def event_generator():
        try:
            input_state = {"user_query": request.query}
            
            # Using astream_events to capture detailed progress
            async for event in vibe_graph.astream_events(input_state, version="v1"):
                kind = event["event"]
                tags = event.get("tags", [])
                metadata = event.get("metadata", {})
                node_name = metadata.get("langgraph_node", "")
                
                # 1. Output from Vibe Analyst (Intermediate Step)
                if kind == "on_chain_end" and node_name == "vibe_analyst":
                    data = event["data"].get("output")
                    if data:
                        yield json.dumps({
                            "type": "analyst_thoughts",
                            "data": data.get("analyst_thoughts", "")
                        }) + "\n"
                        
                        # Also yield keywords for debug/ui if needed
                        yield json.dumps({
                            "type": "analyst_keywords",
                            "data": data.get("refined_keywords", [])
                        }) + "\n"
                
                # 2. Output from Retriever
                elif kind == "on_chain_end" and node_name == "retriever":
                     data = event["data"].get("output")
                     if data:
                        # Yield retrieved products
                        yield json.dumps({
                            "type": "retrieved_products",
                            "data": data.get("retrieved_products", [])
                        }) + "\n"

                # 3. Stream tokens from Stylist (Final Result)
                # We want to catch the LLM stream inside the stylist node
                elif kind == "on_chat_model_stream" and node_name == "stylist":
                    chunk = event["data"]["chunk"]
                    if chunk.content:
                        yield json.dumps({
                            "type": "token",
                            "data": chunk.content
                        }) + "\n"
                        
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield json.dumps({
                "type": "error",
                "data": str(e)
            }) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
