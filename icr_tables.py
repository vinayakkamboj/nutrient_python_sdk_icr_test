import os
from pathlib import Path

from nutrient_sdk import Document, License, Vision, VisionEngine
from nutrient_sdk.vision import VisionError

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value

base_dir = Path(__file__).resolve().parent

if load_dotenv is not None:
    load_dotenv(dotenv_path=base_dir / ".env", override=False)
else:
    load_env_file(base_dir / ".env")
load_env_file(base_dir / ".env.example")

license_key = os.environ.get("NUTRIENT_LICENSE_KEY")
if not license_key:
    raise RuntimeError(
        "Missing NUTRIENT_LICENSE_KEY in environment. "
        "Set it in .env or export it before running the script."
    )
License.register_key(license_key)
input_path = "images.jpeg"
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
