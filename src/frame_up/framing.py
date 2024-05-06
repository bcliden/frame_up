from importlib.resources import as_file, files

from PIL import Image as im
from PIL.Image import Image

border_width = 115


"""
add this attribution:
<a href="https://www.freepik.com/free-photo/old-wooden-frame_976276.htm#fromView=search&page=1&position=1&uuid=549f4e90-bea4-4bf8-a892-ac3baadb811b">Image by mrsiraphol on Freepik</a>
"""

frames: dict[str, Image] = {}
for file in files('frame_up.data').iterdir():
    if file.is_file():
        print("Opening ", file.name)
        img_bytes = file.open("rb")
        image = im.open(img_bytes)
        frames[file.name] = image
    else:
        print("what is this?: ", file.name)

def frame_image(img: Image) -> Image:
    print(frames)
    frame = frames["portrait.jpeg"]
    if img.width > img.height:
        frame = frames["landscape.jpeg"]

    # copy so we don't mutate the original
    frame = frame.copy()

    # get inner dimensions
    up = 0 + border_width
    left = 0 + border_width
    right = frame.width - border_width
    down = frame.height - border_width

    # paste incoming image into the frame
    resized = img.resize((right - left, down - up))

    # probably needs lower right as well
    # or get avg width of frame and add to UL, sub from BR
    frame.paste(resized, box=(up, left))

    return frame
    