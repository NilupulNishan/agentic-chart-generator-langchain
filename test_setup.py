from dotenv import load_dotenv
import os
load_dotenv()

print("API Key loaded    :", bool(os.getenv("AZURE_OPENAI_API_KEY")))
print("Endpoint loaded   :", bool(os.getenv("AZURE_OPENAI_ENDPOINT")))
print("API Version loaded:", bool(os.getenv("AZURE_OPENAI_API_VERSION")))
print("gpt-4o deployment :", os.getenv("AZURE_GPT4O_DEPLOYMENT"))
print("gpt-4o-mini deploy:", os.getenv("AZURE_GPT4O_MINI_DEPLOYMENT"))

import pandas, matplotlib, langgraph, openai
print("\nAll packages imported successfully ✅")