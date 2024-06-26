from pathlib import Path

from frame_up.constants import accepted_image_extensions, version
from frame_up.file import get_suggested_filepath
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPalette

from frame_up_gui.App import FrameUpApp
from frame_up_gui.common import (
    ask_email_contact_info,
    ask_file_to_open,
    ask_file_to_save,
)
from frame_up_gui.events import EventBus as bus
from frame_up_gui.widgets import CentralLayout


class MainWindow(QtWidgets.QMainWindow):
    sourcePath: str

    def __init__(self, *args, **kwargs):
        # pick off the center widget arg if exists
        # center_widget = kwargs["center"]
        # del kwargs["center"]

        super().__init__(*args, **kwargs)

        self.setWindowTitle("Frame-Up")

        self.sourcePath = ""

        @QtCore.Slot(str)
        def updateSourcePath(path: str):
            self.sourcePath = path

        bus.ImagePathChanged.connect(updateSourcePath)

        # enable drag and drop
        self.setAcceptDrops(True)
        self.constructMenuBar()

        self.setCentralWidget(CentralLayout())
        self.resize(400, 300)
        self.show()

        # TODO/bcl: for testing purposes
        self.imagePathChanged(
            "C:/Users/bcliden/Pictures/Grain-Deer-Mushshroom-Environment.png"
        )

    def constructMenuBar(self):
        toolbar = self.menuBar()

        fileMenu = toolbar.addMenu("&File")
        fileMenu.setToolTipsVisible(True)
        fileMenu.setToolTip("File operations: open, save, quit...")

        open_action = QtGui.QAction(text="&Open file", parent=self)
        # button_action.setIcon(QtGui.QIcon("bug.png"))
        open_action.setToolTip("Open a new image file")
        open_action.setStatusTip("Open a new image file")
        open_action.triggered.connect(self.open)
        open_action.setShortcut("Ctrl+O")
        fileMenu.addAction(open_action)

        save_action = QtGui.QAction(text="&Save as...", parent=self)
        # save_action.setIcon(QtGui.QIcon("bug.png"))
        save_action.setToolTip("Save the current image file to a location")
        save_action.setStatusTip("Save the current image file to a location")
        save_action.triggered.connect(self.save_as)
        save_action.setShortcut("Ctrl+S")
        fileMenu.addAction(save_action)

        fileMenu.addSeparator()
        email_action = QtGui.QAction(text="&Email...", parent=self)
        # email_action.setIcon(QtGui.QIcon("bug.png"))
        email_action.setToolTip("Email the current image file")
        email_action.setStatusTip("Email the current image file")
        email_action.triggered.connect(self.email)
        # email_action.setShortcut("Ctrl+E")
        fileMenu.addAction(email_action)
        fileMenu.addSeparator()

        quit_action = QtGui.QAction(text="Quit", parent=self)
        # quit_action.setIcon(QtGui.QIcon("bug.png"))
        quit_action.setStatusTip("Quit the application")
        quit_action.setToolTip("Quit the application")
        quit_action.triggered.connect(self.quit)
        quit_action.setShortcut("Ctrl+Q")
        fileMenu.addAction(quit_action)

        helpMenu = toolbar.addMenu("&Help")
        helpMenu.setToolTipsVisible(True)
        helpMenu.setToolTip("What's going on here?")

        help = QtGui.QAction(text="User Guide", parent=self)
        help.setStatusTip("Looking for some guidance?")
        help.setToolTip("Looking for some guidance?")
        help.triggered.connect(self.help)
        help.setShortcut("F1")
        helpMenu.addAction(help)

        whats_new = QtGui.QAction(text="What's New", parent=self)
        whats_new.setStatusTip("What's new in this version of Frame-Up?")
        whats_new.setToolTip("What's new in this version of Frame-Up?")
        whats_new.triggered.connect(self.whats_new)
        # whats_new.setShortcut("F1")
        helpMenu.addAction(whats_new)

        helpMenu.addSeparator()

        about = QtGui.QAction(text="About", parent=self)
        about.setStatusTip("About this application...")
        about.setToolTip("About this application...")
        about.triggered.connect(self.about)
        about.setShortcut("Ctrl+F1")
        helpMenu.addAction(about)

    """
    Signals
    """

    def imagePathChanged(self, path: str):
        bus.ImagePathChanged.emit(path)

    def exportPathChanged(self, path):
        bus.ExportPathChanged.emit(path)

    """
    Slots
    """

    @QtCore.Slot()
    def open(self):
        name, filter = ask_file_to_open()
        print(f"User picked {name} with applied filter {filter}")
        self.imagePathChanged(name)

    @QtCore.Slot()
    def save_as(self):
        parsed_input = Path(self.sourcePath)
        suggested = get_suggested_filepath(parsed_input.parent, str(parsed_input.name))
        print("we suggested ", suggested)
        filename, filter = ask_file_to_save(str(suggested))
        print(f"User picked {filename} with applied filter {filter}")
        bus.SaveCurrentImage.emit(filename)

    @QtCore.Slot()
    def email(self):
        info = ask_email_contact_info()
        if not info:
            raise SystemError("Couldn't get email contact info from dialog...")
        bus.EmailCurrentImage.emit(info)

    @QtCore.Slot()
    def quit(self):
        FrameUpApp.quit()

    @QtCore.Slot()
    def about(self):
        text = f"""About Frame-Up v.{version}

This application is made by Benjamin Liden <lidenb@oregonstate.edu>
    for CS361: Software Engineering 1 at Oregon State University.

The frame image is by user mrsiraphol on Freepik:
https://www.freepik.com/free-photo/old-wooden-frame_976276.htm
"""
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("About")
        mb.setText(text)
        mb.exec()

    @QtCore.Slot()
    def help(self):
        text = f"""Frame-Up v{version} User Guide
                   
Hello and welcome to the exciting world of picture framing.
With this application, you can load images from your computer
and save them with a new frame around them.

                   
Step 1: 
Select your source image
------------------------
                   
The "Select an Image Source" section contains everything in this step:
    1. A text box showing the currently selected image
    2. A button labeled "Browse..." that opens the system file picker.
                   
Images can be picked from the system dialog using:
    - the top menu at File > Open... 
    - the Browse... button
                   
Once a path has been picked and loaded, you are ready for the next step.
                   
                   
Step 2:
Craft your image
----------------
                
The "Preview Image Frame" shows the current state of the application.
Your selected image from step 1 is visible in the pane here and it is 
framed inside the application's picture frame.

Under "filters", browse and pick the effect you want applied to your image.
The "intensity" slider can be used to fine-tune the effect.
As you change these controls, the preview image will adjust accordingly.
                   

Step 3A:
Save your image
---------------
                   
The "Save your image" section contains the following:
1. A text field showing the suggested file path
2. A "Save" button to immediately save to disk using the suggested path
3. A "Save as..." button for specifying a custom location or filename.
                   
The suggested path will always be a unique one on your disk so your
files won't be overwritten on accident.

Use the "Save as..." button to open the system file dialog
so you can save your image in a custom location with a custom name.

Step 3B:
Email your image
----------------

By pressing the "Email..." button, you can send the current image via email.
A window will appear and ask for the receiver address and the subject line.
The email will be sent in the background once you have confirmed.
"""
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("Help")
        mb.setText(text)
        mb.exec()

    @QtCore.Slot()
    def whats_new(self):
        text = f"""Welcome to v.{version} of Frame-Up...

What's new in this version?

{version}
- Image Filters
    - Antique
    - Vibrant
    - Monochrome
- Email functionality
- User Guide updates
"""
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("What's New")
        mb.setText(text)
        mb.exec()

    """
    Events
    """

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        # can you drop something here? accept or reject
        # show window drop target
        # self.setBackgroundRole(QPalette.ColorRole.Dark)
        md = event.mimeData()

        # are the contents urls
        if md.hasUrls():
            urls = md.urls()

            # is it just one url
            if len(urls) == 1:
                url = md.urls()[0]

                # is it a local file
                if url.isLocalFile():
                    filepath = url.toLocalFile()

                    # is it an accepted extension
                    for extension in accepted_image_extensions:
                        if filepath.lower().endswith(extension):
                            event.accept()
                            return

        event.ignore()

    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent) -> None:
        # hide window drop target
        # self.setBackgroundRole(QPalette.ColorRole.Window)
        return super().dragLeaveEvent(event)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        # handle an accepted drop?
        md = event.mimeData()
        urls = md.urls()

        # should only ever be a single image URL
        assert len(urls) == 1

        for url in urls:
            url_local = url.toLocalFile()
            url_no_scheme = url_local.split("://", maxsplit=1)[
                -1
            ]  # remove the scheme (file://)
            self.imagePathChanged(url_no_scheme)

    def closeEvent(self, *args, **kwargs):
        super().closeEvent(*args, **kwargs)
        FrameUpApp.quit()
