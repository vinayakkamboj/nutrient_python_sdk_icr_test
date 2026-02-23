import os

from nutrient_sdk import Document, Vision
from nutrient_sdk.settings import VlmProvider

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

input_path = "test.pdf"
output_path = "output.json"

if load_dotenv is not None:
    load_dotenv()

with Document.open(input_path) as document:
    # Configure Claude as the VLM provider
    document.settings.vision_settings.provider = VlmProvider.Claude
    api_key = os.environ.get("CLAUDE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing CLAUDE_API_KEY in environment")
    document.settings.claude_api_settings.api_key = api_key

    # Create a vision instance and generate the description
    vision = Vision.set(document)
    description = vision.describe()

    # Save the description to a file
    with open("claude_description.txt", "w", encoding="utf-8") as f:
        f.write(description)
