import os
import base64
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Single shared client (reads from .env) ────────────────────────────────────
client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
)

# ─ Azure Chat deployment
GPT4O_DEPLOYMENT = os.getenv("AZURE_GPT4O_DEPLOYMENT",      "gpt-4o")
GPT4O_MINI_DEPLOYMENT = os.getenv("AZURE_GPT4O_MINI_DEPLOYMENT", "gpt-4o-mini")


def get_response(prompt: str) -> str:
    """
    Send a plain-text prompt to gpt-4o-mini.
    Used by generate_node for code generation.
    Returns the model's reply as a plain string.
    """

    response = client.chat.completions.create(
        model=GPT4O_MINI_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": "You are a data visualization expert who writes clean Python code."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2000,
    )
    return response.choices[0].message.content.strip()


def get_vision_response(prompt: str, media_type: str, b64: str) -> str:
    """
    Send a text prompt + base64 image to gpt-4o (vision).
    Used by reflect_node to critique the chart image.
    Returns the model's reply as a plain string.
    """
    data_url = f"data:{media_type};base64,{b64}"

    response = client.chat.completions.create(
        model = GPT4O_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data visualization expert. "
                    "Respond with a single valid JSON object only. "
                    "Do not include markdown, code fences, or any text outside the JSON."
                )
            },
            {
                "role": "user",
                "content":[
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url":{
                            "url": data_url,
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=2000,
    )
    return response.choices[0].message.content.strip()
