import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")

from state import ChartAgentState
from nodes.generate_node import generate_node
from nodes.execute_node import execute_v1_node
from nodes.reflect_node import reflect_node

# ── Run nodes 1 and 2 first to get chart_v1.png ───────────────────────────────
print("Step 1 — generate_node...")
state: ChartAgentState = {
    "dataset_path":   "data/coffee_sales.csv",
    "instruction":    "Create a bar chart comparing total Q1 coffee sales revenue in 2024 vs 2025 by coffee type.",
    "image_basename": "chart",
}
state = generate_node(state)
state = execute_v1_node(state)

if state.get("error"):
    print(f"❌ Setup failed: {state['error']}")
    exit(1)

print("✅ V1 chart ready\n")

# ── Now test reflect_node ─────────────────────────────────────────────────────
print("Step 2 — reflect_node (vision call to gpt-4o)...")
state = reflect_node(state)

if state.get("error"):
    print(f"❌ reflect_node failed: {state['error']}")
    exit(1)

print(f"\n✅ reflect_node succeeded!")
print(f"\n--- FEEDBACK ---")
print(state["feedback"])
print(f"\n--- CODE V2 (first 500 chars) ---")
print(state["code_v2"][:500])
print(f"\n   chart_v2_path : {state['chart_v2_path']}")