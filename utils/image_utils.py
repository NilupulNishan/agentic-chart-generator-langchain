import re
import base64
import mimetypes

def encode_image_b64(path: str) -> tuple[str, str]:
    """
    Read an image file and return (media_type, base64_string).
    Used to send chart image to the vision LLM."""
    mime, _ = mimetypes.guess_type(path)
    media_type = mime or "image/png"

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    return media_type, b64


def extract_code_block(text: str) -> str:
    """
    Pull out the Python code inside <execute_python>...</execute_python> tags.
    Returns the raw code string, or empty string if tags not found.
    """
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", text)
    return match.group(1).strip() if match else "" 


def ensure_execute_python_tags(text: str) -> str:
    """
    Guarantee the code is wrapped in <execute_python> tags.
    Strips markdown fences (```python) if the LLM added them anyway.
    """
    text = text.strip()
    # Strip markdown code fences if present
    text = re.sub(r"^```(?:python)?\s*|\s*```$", "", text).strip()
    
    if "<execute_python>" not in text:
        text = f"<execute_python>\n{text}\n</execute_python>"

    return text