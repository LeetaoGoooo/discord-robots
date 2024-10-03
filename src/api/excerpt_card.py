from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
from dataclasses_json import dataclass_json
from typing import Dict
from jinja2 import FileSystemLoader, Environment
from .utils import html2img_with_selector, str2qrcode,img2base64

work_dir = Path.cwd()

@dataclass_json
@dataclass
class ExcerptCard:
    title: Optional[str]
    author: Optional[str]
    created_at: Optional[str]
    excerpt: str
    theme: Optional[int]
    qr_code: Optional[str]


def excerpt_card(user_input: Dict) -> Path:
    excerpt_card_input = ExcerptCard.from_dict(user_input)
    environment = Environment(loader=FileSystemLoader(work_dir.joinpath("api/templates/")))
    template = environment.get_template("excerpt_card.html")
    if excerpt_card_input.qr_code:
        try:
            qr_code_path = str2qrcode(excerpt_card_input.qr_code)
            base64img_str = img2base64(qr_code_path)
            excerpt_card_input.qr_code = base64img_str
            qr_code_path.unlink(missing_ok=True)
        except Exception as e:
            print("generate qrcode failed", e)
            return
    card = template.render(excerpt_card=excerpt_card_input)
    return html2img_with_selector(card, "excerpt_card")    