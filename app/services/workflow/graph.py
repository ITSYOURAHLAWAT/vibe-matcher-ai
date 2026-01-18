from langgraph.graph import StateGraph, END

from app.services.workflow.state import GraphState
from app.services.workflow.nodes import vibe_analyst_node, retriever_node, stylist_node

def create_workflow():
    """
    Constructs the Vibe Matcher LangGraph.
    """
    workflow = StateGraph(GraphState)
    
    # Add Nodes
    workflow.add_node("vibe_analyst", vibe_analyst_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("stylist", stylist_node)
    
    # Define Edges
    workflow.set_entry_point("vibe_analyst")
    workflow.add_edge("vibe_analyst", "retriever")
    workflow.add_edge("retriever", "stylist")
    workflow.add_edge("stylist", END)
    
    return workflow.compile()

# Singleton graph instance
vibe_graph = create_workflow()
