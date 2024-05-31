from dataclasses import dataclass
from typing import Optional, Type

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialogButtonBox

default_width = 300  # px?
default_height = 100  # px?


@dataclass
class EmailContactInfo:
    to: str
    subject: str


class EmailDialog(QtWidgets.QDialog):
    """
    Get email "to" and "subject" from user
    """

    info: Optional[EmailContactInfo]
    to: str
    subject: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = None
        self.to = ""
        self.subject = ""

        # widgets
        to_field = QtWidgets.QLineEdit()
        to_field.setPlaceholderText("jane.doe@example.com")

        subject_field = QtWidgets.QLineEdit()
        subject_field.setPlaceholderText("Check out this cool image")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        # actions
        to_field.textEdited.connect(self.set_to)
        subject_field.textEdited.connect(self.set_subject)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # layout
        layout = QtWidgets.QFormLayout()
        layout.addRow("To:", to_field)
        layout.addRow("Subject:", subject_field)
        layout.addWidget(buttons)

        # configuration
        self.setLayout(layout)
        self.resize(default_width, default_height)
        self.setMaximumHeight(default_height)

        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setWindowTitle("Please provide email details...")

    def get_form_data(self) -> Optional[EmailContactInfo]:
        return self.info

    @QtCore.Slot(str)
    def set_to(self, to: str):
        self.to = to

    @QtCore.Slot(str)
    def set_subject(self, subject: str):
        self.subject = subject

    @QtCore.Slot()
    def accept(self) -> None:
        to = self.to
        subject = self.subject
        if not len(to) or not len(subject):
            return self.reject()
        else:
            self.info = EmailContactInfo(to, subject)
            return super().accept()

    @QtCore.Slot()
    def reject(self):
        self.info = None
        return super().reject()

    @classmethod
    def get_email_info(cls: Type["EmailDialog"]) -> Optional[EmailContactInfo]:
        instance = cls()
        instance.exec()
        return instance.get_form_data()
