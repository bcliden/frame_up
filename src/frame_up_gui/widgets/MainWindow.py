from typing import Any
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette

from frame_up.constants import home_dir, accepted_image_extensions
from frame_up_gui.widgets import CentralLayout
from frame_up_gui.events import ImagePathChanged, ExportPathChanged
from frame_up_gui.common import open_file_name, get_save_file_name

class MainWindow(QtWidgets.QMainWindow):
    # imagePathChangeEvent: ImagePathChangedClass

    def __init__(self, *args, **kwargs):
        # pick off the center widget arg if exists
        # center_widget = kwargs["center"]
        # del kwargs["center"]

        super().__init__(*args, **kwargs)

        self.setWindowTitle("Frame-Up")
        # manifest["main"] = self

        # if center_widget is not None:
        #     self.setCentralWidget(center_widget)
        # else:
        #     print("You forgot to pass a central widget to MainWindow")

        # enable draggo and droppo
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

        quit_action = QtGui.QAction(text="Quit", parent=self)
        # quit_action.setIcon(QtGui.QIcon("bug.png"))
        quit_action.setStatusTip("Quit the application")
        quit_action.setToolTip("Quit the application")
        quit_action.triggered.connect(self.quit)
        quit_action.setShortcut("Ctrl+Q")
        fileMenu.addAction(quit_action)

        # editMenu = toolbar.addMenu("&Edit")
        # editMenu.setToolTipsVisible(True)
        # editMenu.setToolTip("Edit the current operations")
        # editMenu.addAction(open_action)
        # editMenu.addAction(save_action)
        # editMenu.addSeparator()
        # editMenu.addAction(quit_action)

        # toolbar.addSeparator()

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
    def imagePathChanged(self, path):
        ImagePathChanged.change(path)

    def exportPathChanged(self, path):
        ExportPathChanged.change(path)


    """
    Slots
    """

    @QtCore.Slot(Any)
    def open(self):
        name, filter = open_file_name()
        print(f"User picked {name} with applied filter {filter}")
        self.imagePathChanged(name)

    @QtCore.Slot(Any)
    def save_as(self):
        fileName, filter = get_save_file_name()
        print(f"User picked {fileName} with applied filter {filter}")
        self.exportPathChanged(fileName)

    @QtCore.Slot(Any)
    def quit(self):
        # app.quit()                    # needs a reference to the app
        # QtWidgets.QApplication.quit()   # also works?
        self.close()                    # maybe the best... ?

    @QtCore.Slot(Any)
    def about(self):
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("About")
        mb.setText("Here are some fun facts about me... <also attributions>")
        mb.exec()

    @QtCore.Slot(Any)
    def help(self):
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("Help")
        mb.setText("Let's see if we can clear this up...")
        mb.exec()

    @QtCore.Slot(Any)
    def whats_new(self):
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("What's New")
        mb.setText("Welcome to v.XYZ of Frame-Up...")
        mb.exec()

    """
    Events
    """

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        # can you drop something here? accept or reject
        # show window drop target
        self.setBackgroundRole(QPalette.ColorRole.Dark)
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
        self.setBackgroundRole(QPalette.ColorRole.Window)
        return super().dragLeaveEvent(event)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        # handle an accepted drop?
        md = event.mimeData()
        urls = md.urls()

        # should only ever be a single image URL
        for url in urls:
            print("dropped: ", url)
            self.imagePathChanged(url)
