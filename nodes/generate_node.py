"""Node 1 — Generate V1 chart code."""
import logging
from state import ChartAgentState
from utils import get_response, load_and_prepare_data, make_schema_text

logger = logging.getLogger(__name__)

GENERATE_PROMPT = """
You are a data visualization expert.

Return your answer *strictly* in this format and nothing else:

<execute_python>
# your python code here
</execute_python>

Do NOT add any explanation, comments outside the tags, or markdown.

The code should create a visualization from a DataFrame 'df' with this schema:
{schema}

User instruction: {instruction}

Requirements:
1. Assume the DataFrame is already loaded as 'df'. Do NOT read any CSV file.
2. Use matplotlib only (no seaborn).
3. Add a clear title, axis labels, and legend where appropriate.
4. Save the figure to '{out_path}' with dpi=150.
5. Do NOT call plt.show().
6. Call plt.close() at the very end.
7. Include ALL necessary import statements inside the tags.
"""

def generate_node(state: ChartAgentState) -> ChartAgentState:
    """
    LangGraph Node 1 — generates first-draft chart code (V1).

    Reads  : dataset_path, instruction, image_basename
    Writes : df, code_v1, chart_v1_path
    """

    logger.info(f" [generate_node] Loading dataset and generating V1 code...")

    # Load Data
    df = load_and_prepare_data(state["dataset_path"])
    schema = make_schema_text(df)

    # Build output path
    basename = state.get("image_basename")
    out_path = f"outputs/{basename}_v1.png"

    # Build prompt
    prompt = GENERATE_PROMPT.format(
        schema=schema,
        instruction=state["instruction"],
        out_path=out_path,
    )

    # Call gpt-4o-mini
    try:
        code_v1 = get_response(prompt)
        logger.info("✅  [generate_node] V1 code received (%d chars)", len(code_v1))
    except Exception as exc:
        logger.error("❌  [generate_node] LLM call failed: %s", exc)
        return {**state, "error": str(exc)}
    
    return {
        **state,
        "df": df,
        "code_v1": code_v1,
        "chart_v1_path": out_path
    }
        
