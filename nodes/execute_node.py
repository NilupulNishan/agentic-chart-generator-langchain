"""Node 2 & 4 — Execute generated chart code."""

import os
import logging
from state import ChartAgentState
from utils import extract_code_block

logger = logging.getLogger(__name__)

def _run_code(code_tagged: str, df, out_path: str, version: str) -> str | None:
    """
    Extract code from tags and exec() it.
    Returns error message string on faliure, None on success."""

    # Extract code from tags
    code = extract_code_block(code_tagged)
    if not code:
        msg = f"No <execute_python> block found in {version} code."
        logger.error("❌  [execute_node] %s", msg)
        return msg
    
    # Ensure output directory exist
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # # ── Patch any wrong output path the LLM may have written ─────────────────
    # # LLMs sometimes write 'output/' instead of 'outputs/' — fix it silently
    # code = code.replace("'output/", f"'{os.path.dirname(out_path)}/")
    # code = code.replace('"output/', f'"{os.path.dirname(out_path)}/')

    # # ── Force the correct output path regardless of what LLM wrote ───────────
    # import re
    # code = re.sub(
    #     r"plt\.savefig\(['\"].*?['\"]",
    #     f"plt.savefig('{out_path}'",
    #     code
    # )

    logger.info("💻  [execute_node] Running %s code → %s", version, out_path)

    try:
        exec_globals = {"df": df}
        exec(code, exec_globals)  # noqa: S102
        logger.info("✅  [execute_node] %s chart saved → %s", version, out_path)
        return None
    except Exception as exc:
        logger.error("❌  [execute_node] %s execution failed: %s", version, exc)
        return f"{version} execution error: {exc}"
    

def execute_v1_node(state: ChartAgentState) -> ChartAgentState:
    """
    LangGraph Node 2 — executes V1 code and saves the chart.

    Reads  : code_v1, df, chart_v1_path
    Writes : chart file on disk / error in state
    """
    error = _run_code(
        code_tagged=state["code_v1"],
        df=state["df"],
        out_path=state["chart_v1_path"],
        version="V1",
    )
    if error:
        return {**state, "error": error}
    return state


def execute_v2_node(state: ChartAgentState) -> ChartAgentState:
    """
    LangGraph Node 4 — executes V2 refined code and saves the chart.

    Reads  : code_v2, df, chart_v2_path
    Writes : chart file on disk / error in state
    """
    error = _run_code(
        code_tagged=state["code_v2"],
        df=state["df"],
        out_path=state["chart_v2_path"],
        version="V2",
    )
    if error:
        return {**state, "error": error}
    return state