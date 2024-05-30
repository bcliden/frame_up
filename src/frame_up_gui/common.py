from typing import Optional

from frame_up.constants import home_dir
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QFileDialog

from frame_up_gui.widgets.EmailDialog import EmailContactInfo, EmailDialog


def open_file_name() -> tuple[str, str]:
    return QFileDialog.getOpenFileName(
        # parent=parent,
        caption="Select an image",
        dir=home_dir,  # though maybe this should be the source dir
        filter="Images (*.png *.jpg *.jpeg)",
        selectedFilter="Images (*.png *.jpg *.jpeg)",
    )


def get_save_file_name(suggested: Optional[str] = None) -> tuple[str, str]:
    if suggested is None:
        suggested = home_dir

    return QtWidgets.QFileDialog.getSaveFileName(
        # parent=self,
        caption="Open image",
        # though maybe this should be the source dir
        # or even /path/to/original/image/smiley{_framed}.ext
        # or an auto-incrementing file name like smiley_framed_<n>.ext
        dir=suggested,
        filter="Images (*.png *.jpg *.jpeg)",
        selectedFilter="Images (*.png *.jpg *.jpeg)",
    )


def get_email_contact_info() -> EmailContactInfo:
    """write custom email dialog? ugh"""
    dialog = EmailDialog()
    dialog.exec()  # doesn't matter if it succeeds...
    return dialog.get_info()
