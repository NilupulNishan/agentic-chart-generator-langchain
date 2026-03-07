import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")

from graph import build_graph

print("Building graph...")
graph = build_graph()

# ── Print the graph structure ─────────────────────────────────────────────────
print("\n--- Graph Structure ---")
print(graph.get_graph().draw_mermaid())
print()

print("✅ graph.py compiled successfully!")