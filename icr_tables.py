import os

from nutrient_sdk import Document, License, Vision, VisionEngine
from nutrient_sdk.vision import VisionError

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()

license_key = os.environ.get("NUTRIENT_LICENSE_KEY")
if not license_key:
    raise RuntimeError("Missing NUTRIENT_LICENSE_KEY in environment")
License.register_key(license_key)
input_path = "sample.png"
output_path = "output.json"

with Document.open(input_path) as document:
    document.settings.vision_settings.engine = VisionEngine.VLM_ENHANCED_ICR
    vision = Vision.set(document)

    try:
        content_json = vision.extract_content()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content_json)
        print(f"Extraction complete: {output_path}")
    except VisionError as err:
        print(f"Vision extraction failed: {err}")
