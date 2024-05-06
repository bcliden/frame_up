from pathlib import Path

accepted_image_mime_types = ["image/jpeg", "image/png"]  # no "image/jpg" exists
accepted_image_extensions = [".jpg", ".jpeg", ".png"]
home_dir = str(Path.home())  # this is the user's home dir

default_extension = ".jpg"