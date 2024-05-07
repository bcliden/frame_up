from pathlib import Path

# todo: make this dynamic?
version = "0.0.1"

accepted_image_mime_types = ["image/jpeg", "image/png"]  # no "image/jpg" exists
accepted_image_extensions = [".jpg", ".jpeg", ".png"]
home_dir = str(Path.home())  # this is the user's home dir

default_extension = ".jpg"