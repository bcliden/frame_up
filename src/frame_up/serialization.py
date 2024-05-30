from base64 import b64decode, b64encode
from io import BytesIO

from PIL import Image as im
from PIL.Image import Image


def base64_encode_image(image: Image) -> str:
    bio = BytesIO()
    image.save(bio)
    return b64encode(bio.getvalue()).decode("utf-8")


def base64_decode_image(text: str) -> Image:
    img_bytes = b64decode(text)
    img_bio = BytesIO(img_bytes)
    image = im.open(img_bio)
    image.load()  # just in case?
    return image
