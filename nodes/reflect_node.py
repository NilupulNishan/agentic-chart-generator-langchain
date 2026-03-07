"""Node 3 — Reflect on V1 chart and generate improved V2 code."""
import re
import json
import logging

from state import ChartAgentState
from utils import encode_image_b64, get_vision_response, ensure_execute_python_tags

logger = logging.getLogger(__name__)

REFLECT_PROMPT = """

You are a data visualization expert reviewing a chart and its code.

Your Task:
1. Critique the attached chart against the user instruction
2. Return imporved matplotlib code that fixes all issues found.

Original code (for context):
{code_v1}

OUTPUT FORMAT - Follow this EXACTLY, two parts only, nothing else:

PART 1 — First line must be a valid JSON object with ONLY a "feedback" field:
{{"feedback": "your critique here — be specific about what is wrong and what to improve"}}

PART 2 — After a blank line, the refined Python code wrapped in tags:
<execute_python>
# improved code here
</execute_python>

HARD CONSTRAINTS:
- No markdown, no backticks, no prose outside these two parts.
- Use pandas + matplotlib only. No seaborn.
- Assume df already exists. Do NOT read any CSV file.
- Save the figure to '{out_path}' with dpi=150.
- Call plt.close() at the end. No plt.show().
- Include ALL import statements inside the tags.
- Fix every issue mentioned in the feedback.

DataFrame schema:
{schema}

User instruction:
{instruction}
"""

def reflect_node(state: ChartAgentState) -> ChartAgentState:
    """
    LangGraph Node 3 — critiques V1 chart image and produces refined V2 code.

    Reads  : chart_v1_path, code_v1, instruction, image_basename, df
    Writes : feedback, code_v2, chart_v2_path
    """
    logger.info("🔁  [reflect_node] Encoding chart and calling gpt-4o vision...")

    # Build paths
    basename = state.get("image_basename", "chart")
    out_path = f"outputs/{basename}_v2.png"

    # Build schema from df
    from utils import make_schema_text
    schema = make_schema_text(state["df"])

    # Encode the V1 chart image
    try:
        media_type, b64 = encode_image_b64(state["chart_v1_path"])
        logger.info("🖼️   [reflect_node] Image encoded (%d b64 chars)", len(b64))
    except FileNotFoundError as exc:
        logger.error("❌  [reflect_node] Chart image not found: %s", exc)
        return {**state, "error": str(exc)}
    
    # Build prompt
    prompt = REFLECT_PROMPT.format(
        code_v1 = state["code_v1"],
        out_path = out_path,
        schema = schema,
        instruction =  state["instruction"]
    )

    # Call gpt-4ovision
    try:
        content = get_vision_response(prompt, media_type, b64)
        logger.info("✅  [reflect_node] Vision response received (%d chars)", len(content))

    except Exception as exc:
        logger.error("❌  [reflect_node] Vision LLM call failed: %s", exc)
        return {**state, "error": str(exc)}
    
    # Parse feedback from first JSON line
    feedback = _parse_feedback(content)
    logger.info("💬  Feedback: %s", feedback)

    # Extract refined code from <execute_python> tags
    m_code = re.search(r"<execute_python>([\s\S]*?)</execute_python>", content)
    refined_body = m_code.group(1).strip() if m_code else ""
    code_v2 = ensure_execute_python_tags(refined_body)

    if not refined_body:
        logger.warning("⚠️   [reflect_node] No code block found in vision response!")
        logger.warning("    Raw response: %s", content[:500])

    logger.info("📝  [reflect_node] V2 code extracted (%d chars)", len(refined_body))

    return {
        **state,
        "feedback":      feedback,
        "code_v2":       code_v2,
        "chart_v2_path": out_path,
    }


def _parse_feedback(content: str) -> str:
    """
    Robustly extract the feedback string from the LLM response.
    Tries 3 methods -
    """
    # Strategy 1: parse the first line as JSON
    lines = content.strip().splitlines()
    first_line = lines[0].strip() if lines else ""
    try:
        obj = json.loads(first_line)
        return str(obj.get("feedback", "")).strip()
    except json.JSONDecodeError:
        pass

    # Strategy 2: find first {...} block anywhere in response
    m = re.search(r"\{.*?\}", content, flags=re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            return str(obj.get("feedback", "")).strip()
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: return raw content up to the code block as feedback
    before_code = content.split("<execute_python>")[0].strip()
    return before_code[:300] if before_code else "No feedback parsed."
    


