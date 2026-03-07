"""
Defines and compiles the LangGraph StateGraph.
"""

import logging
from langgraph.graph import StateGraph, END
from typing import Literal

from state import ChartAgentState
from nodes import generate_node, execute_v1_node, reflect_node, execute_v2_node

logger = logging.getLogger(__name__)

def _should_continue(state:  ChartAgentState) ->  Literal["continue", "end"]:
    """If any node set an error → route to END immediately."""
    if state.get("error"):
        logger.error("⛔ Error detected, stopping graph: %s", state["error"])
        return "end"
    return "continue"

def build_graph():
    """Build and compile the chart generation + reflection workflow."""

    builder = StateGraph(ChartAgentState)

    # Register all nodes
    builder.add_node("generate", generate_node)
    builder.add_node("execute_v1", execute_v1_node)
    builder.add_node("reflect", reflect_node)
    builder.add_node("execute_v2", execute_v2_node)
    
    # Entry point
    builder.set_entry_point("generate")
    
    # Edges with error guard after each node
    builder.add_conditional_edges(
        "generate",
        _should_continue,
        {"continue": "execute_v1", "end": END}
    )

    builder.add_conditional_edges(
        "execute_v1",
        _should_continue,
        {"continue": "reflect", "end": END},
    )
    builder.add_conditional_edges(
        "reflect",
        _should_continue,
        {"continue": "execute_v2", "end":END},
    )

    # Final node always goes to END
    builder.add_edge("execute_v2", END)

    return builder.compile()