from dataclasses import dataclass
from typing import Optional

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialogButtonBox


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

        # layouts

        # TODO/bcl: QFormLayout instead?

        # widgets
        to_text = QtWidgets.QLabel("To Address: ")
        to_field = QtWidgets.QLineEdit()
        to_field.setPlaceholderText("jane.doe@example.com")
        subject_text = QtWidgets.QLabel("Subject: ")
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

        # organization
        email_group = QtWidgets.QGroupBox("Provide email information")

        group_layout = QtWidgets.QGridLayout(email_group)
        group_layout.addWidget(to_text, 0, 0)
        group_layout.addWidget(to_field, 0, 1, 1, 4)
        group_layout.addWidget(subject_text, 1, 0)
        group_layout.addWidget(subject_field, 1, 1, 1, 4)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(email_group)
        main_layout.addWidget(buttons)

        self.setLayout(main_layout)
        self.setWindowTitle("Email Info Dialog")

    def get_info(self) -> Optional[EmailContactInfo]:
        return self.info

    @QtCore.Slot(str)
    def set_to(self, to: str):
        self.to = to

    @QtCore.Slot(str)
    def set_subject(self, subject: str):
        self.subject = subject

    @QtCore.Slot(None)
    def accept(self) -> None:
        to = self.to
        subject = self.subject
        if not len(to) or not len(subject):
            return self.reject()
        else:
            self.info = EmailContactInfo(to, subject)
            return super(EmailDialog, self).accept()

    @QtCore.Slot(None)
    def reject(self):
        self.info = None
        return super(EmailDialog, self).reject()
