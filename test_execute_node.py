import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")

from state import ChartAgentState
from nodes.generate_node import generate_node
from nodes.execute_node import execute_v1_node
import os

# ── Step 1: run generate_node to get real code ────────────────────────────────
print("Step 1 — Running generate_node...")
state: ChartAgentState = {
    "dataset_path":   "data/coffee_sales.csv",
    "instruction":    "Create a bar chart comparing total Q1 coffee sales revenue in 2024 vs 2025 by coffee type.",
    "image_basename": "chart",
}
state = generate_node(state)

if state.get("error"):
    print(f"❌ generate_node failed: {state['error']}")
    exit(1)

print(f"✅ generate_node OK — code_v1 length: {len(state['code_v1'])} chars")
print()

# ── Step 2: run execute_v1_node ───────────────────────────────────────────────
print("Step 2 — Running execute_v1_node...")
state = execute_v1_node(state)

if state.get("error"):
    print(f"❌ execute_v1_node failed: {state['error']}")
    exit(1)

# ── Verify chart was saved ────────────────────────────────────────────────────
chart_path = state["chart_v1_path"]
if os.path.exists(chart_path):
    size_kb = os.path.getsize(chart_path) / 1024
    print(f"✅ execute_v1_node OK!")
    print(f"   Chart saved : {chart_path}")
    print(f"   File size   : {size_kb:.1f} KB")
else:
    print(f"❌ Chart file not found at: {chart_path}")