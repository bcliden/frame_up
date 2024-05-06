from pathlib import Path

from PIL import Image as im
from PIL.Image import Image

from frame_up.constants import default_extension


def save_to_disk(path: str, image: Image, *, format=None):
    if format is None:
        format = default_extension
    print(f"Saving an image to {path} with format {format}")
    image.save(path, format=format)

def open_from_disk(path: str) -> Image:
    return im.open(path)

def get_suggested_filepath(directory: Path, filename: str) -> Path:
    path = directory / filename

    if path.exists():
        name, ext = filename.rsplit(".", maxsplit=1)
        try:
            # is it in this program's format?
            name, middle, idx = name.rsplit("_", maxsplit=2)
            if middle != "framed":
                raise ValueError("middle portion is actually ", middle)
            idx = int(idx) + 1
        except ValueError as e:
            print(e)
            # may not have been in initial format
            idx = 0
        return get_suggested_filepath(directory, f"{name}_framed_{idx}.{ext}")

    return path
