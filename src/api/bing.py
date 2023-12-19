from typing import List
from BingImageCreator import ImageGen 
import os


def create_image(prompt:str) -> List[str]:
    cookie = os.getenv("BING_TOKEN")
    image_gen = ImageGen(cookie)
    images = image_gen.get_images(prompt)
    return images