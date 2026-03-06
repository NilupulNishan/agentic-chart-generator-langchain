import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")

from state import ChartAgentState
from nodes.generate_node import generate_node

# ── Build the minimal state generate_node needs ───────────────────────────────
initial_state: ChartAgentState = {
    "dataset_path":  "data/coffee_sales.csv",
    "instruction":   "Create a bar chart comparing total Q1 coffee sales revenue in 2024 vs 2025 by coffee type.",
    "image_basename": "chart",
}

print("Running generate_node...")
result = generate_node(initial_state)

# ── Check for errors ──────────────────────────────────────────────────────────
if result.get("error"):
    print(f"❌ Error: {result['error']}")
else:
    print(f"\n✅ generate_node succeeded!")
    print(f"   chart_v1_path : {result['chart_v1_path']}")
    print(f"   df shape      : {result['df'].shape}")
    print(f"\n--- code_v1 output ---")
    print(result["code_v1"])