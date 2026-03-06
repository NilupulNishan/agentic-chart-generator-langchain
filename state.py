"""
Defines the shared state TypedDict that flows through every
LangGraph node. Nodes read from it and write back to it.

This work as the "memory" of the entire workflow.
"""
from typing import Optional
from typing_extensions import TypedDict
import pandas as pd

class ChartAgentState(TypedDict, total=False):

    # ── Inputs (set once at the start by main.py) ────────────────────────────
    dataset_path:  str   # e.g. "data/coffee_sales.csv"
    instruction:   str   # natural-language chart request from the user
    image_basename: str  # e.g. "chart" → outputs/chart_v1.png, chart_v2.png

    # ── Data (loaded inside generate_node) ───────────────────────────────────
    df: Optional[object]  # the loaded pandas DataFrame

    # ── V1 artifacts (produced by generate_node + execute_v1_node) ───────────
    code_v1:       str   # raw LLM output including <execute_python> tags
    chart_v1_path: str   # e.g. "outputs/chart_v1.png"

    # ── Reflection artifacts (produced by reflect_node) ───────────────────────
    feedback:      str   # LLM critique of the V1 chart

    # ── V2 artifacts (produced by reflect_node + execute_v2_node) ────────────
    code_v2:       str   # refined code including <execute_python> tags
    chart_v2_path: str   # e.g. "outputs/chart_v2.png"

     # ── Error tracking ────────────────────────────────────────────────────────
    error: Optional[str]  # any node sets this on failure → graph stops cleanly