from utils.llm_clients import get_response, get_vision_response, GPT4O_DEPLOYMENT, GPT4O_MINI_DEPLOYMENT
import matplotlib.pyplot as plt
from utils.image_utils import encode_image_b64

print(f"Generation model : {GPT4O_MINI_DEPLOYMENT}")
print(f"Reflection model : {GPT4O_DEPLOYMENT}")
print()

# ── Test 1: plain text call (gpt-4o-mini) ─────────────────────────────────────
print("Test 1 — get_response (gpt-4o-mini):")
reply = get_response("Say hello and tell me which model you are in one sentence.")
print(f"  Reply: {reply}")
print()

# ── Test 2: vision call (gpt-4o) ──────────────────────────────────────────────
print("Test 2 — get_vision_response (gpt-4o):")

# Create a simple test chart to send
plt.figure(figsize=(4, 3))
plt.bar(["Coffee", "Latte", "Espresso"], [120, 95, 80])
plt.title("Test Chart")
plt.savefig("outputs/test_vision.png", dpi=72)
plt.close()

media_type, b64 = encode_image_b64("outputs/test_vision.png")
vision_reply = get_vision_response(
    prompt='Describe this chart in one sentence. Return JSON: {"feedback": "your description here"}',
    media_type=media_type,
    b64=b64
)
print(f"  Reply: {vision_reply}")
print()
print("All LLM client tests passed ✅")