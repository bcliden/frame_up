from typing import Final, Optional

from frame_up.constants import home_dir
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from frame_up_gui.widgets.EmailDialog import EmailContactInfo, EmailDialog

image_filter: Final[str] = "Images (*.png *.jpg *.jpeg)"


def ask_file_to_open() -> tuple[str, str]:
    return QFileDialog.getOpenFileName(
        # parent=parent,
        caption="Select an image",
        dir=home_dir,  # though maybe this should be the source dir
        filter=image_filter,
        selectedFilter=image_filter,
    )


def ask_file_to_save(suggested: Optional[str] = None) -> tuple[str, str]:
    if suggested is None:
        suggested = home_dir

    return QtWidgets.QFileDialog.getSaveFileName(
        # parent=self,
        caption="Open image",
        # though maybe this should be the source dir
        # or even /path/to/original/image/smiley{_framed}.ext
        # or an auto-incrementing file name like smiley_framed_<n>.ext
        dir=suggested,
        filter=image_filter,
        selectedFilter=image_filter,
    )


def ask_email_contact_info() -> EmailContactInfo:
    info = EmailDialog.get_email_info()
    if info is None:
        raise SystemError("Couldn't get info from email dialog")
    return info
