"""Entry point for the Chart Generation Agentic Workflow."""

import os 
import sys
import logging
import  argparse

# Logging setup 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chart Generation Agentic Workflow - LangGraph + Azure OpenAI"
    )
    parser.add_argument(
        "--instruction",
        default="Create a bar chart comparing total Q1 coffee sales revenue in 2024 vs 2025 by coffee type.",
        help="Natural-language chart request.",
    )
    parser.add_argument(
        "--dataset",
        default="data/coffee_saled.csv",
        help="Path to the input CSV file."
    )
    parser.add_argument(
        "--image-basename"
        default="chart",
        help="Base name for output images. e.g. 'chart' → outputs/chart_v1.png, chart_v2.png",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    # - Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)

    # - Import graph after args (keeps startup fast)
    from graph import build_graph
    from state import ChartAgentState

    # - Print run summery
    logger.info("=" * 65)
    logger.info("  Chart Generation Agentic Workflow")
    logger.info("=" * 65)
    logger.info("  Instruction      : %s", args.instruction)
    logger.info("  Dataset          : %s", args.dataset)
    logger.info("  Image basename   : %s", args.image_basename)
    logger.info("  Generation model : gpt-4o-mini")
    logger.info("  Reflection model : gpt-4o")
    logger.info("=" * 65)

    # - Build the graph
    graph = build_graph()

    # - Set initial state
    initial_state: ChartAgentState = {
        "dataset_path":   args.dataset,
        "instruction":    args.instruction,
        "image_basename": args.image_basename,
    }

    # - Run the full workflow
    logger.info("🚀  Starting workflow...\n")
    final_state = graph.invoke(initial_state)

    # - Report results
    logger.info("\n" + "=" * 65)

    if final_state.get("error"):
        logger.error("⛔  Workflow failed: %s", final_state["error"])
        sys.exit(1)

    logger.info("✅  Workflow completed successfully!")
    logger.info("")
    logger.info("  📊 V1 chart  : %s", final_state.get("chart_v1_path"))
    logger.info("  💬 Feedback  :")

    # - Print feedback on multiple lines if long
    feedback = final_state.get("feedback", "")
    for line in feedback.split(". "):
        if line.strip():
            logger.info("      %s.", line.strip())

    logger.info("")
    logger.info("  📊 V2 chart  : %s", final_state.get("chart_v2_path"))
    logger.info("=" * 65)

if __name__ == "__main__":
    main()

