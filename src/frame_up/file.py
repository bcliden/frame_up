from PIL import Image as im
from PIL.Image import Image

from frame_up.constants import default_extension


def save_to_disk(path: str, image: Image, /, format):
    if format is None:
        format = default_extension
    image.save(path, format=format)

def open_from_disk(path: str) -> Image:
    return im.open(path)
