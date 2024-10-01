import base64
from pathlib import Path

def img2base64(img_path:Path) -> str:
    if not img_path.exists():
        raise FileNotFoundError
    with open(img_path,'rb') as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")