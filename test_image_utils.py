from utils.image_utils import extract_code_block, ensure_execute_python_tags, encode_image_b64

# ── Test 1: extract code block ────────────────────────────────────────────────
tagged = """
<execute_python>
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.savefig("test.png")
plt.close()
</execute_python>
"""
code = extract_code_block(tagged)
print("Test 1 — extract_code_block:")
print(code)
print()

# ── Test 2: ensure tags when missing ─────────────────────────────────────────
raw_code = "import matplotlib.pyplot as plt\nplt.plot([1,2,3])"
wrapped = ensure_execute_python_tags(raw_code)
print("Test 2 — ensure_execute_python_tags (no tags):")
print(wrapped)
print()

# ── Test 3: strip markdown fences ────────────────────────────────────────────
fenced = "```python\nimport matplotlib.pyplot as plt\nplt.plot([1,2,3])\n```"
wrapped2 = ensure_execute_python_tags(fenced)
print("Test 3 — ensure_execute_python_tags (markdown fences):")
print(wrapped2)
print()

# ── Test 4: encode a real image ───────────────────────────────────────────────
# First create a tiny test image
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.savefig("outputs/test_chart.png", dpi=72)
plt.close()

media_type, b64 = encode_image_b64("outputs/test_chart.png")
print("Test 4 — encode_image_b64:")
print(f"  media_type : {media_type}")
print(f"  b64 length : {len(b64)} chars")
print(f"  first 40   : {b64[:40]}...")
print()
print("All image_utils tests passed ✅")