from pathlib import Path
from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette

from frame_up.file import save_to_disk, get_suggested_filepath
from frame_up_gui.events import ImagePathChanged, ExportPathChanged, SaveCurrentImage
from frame_up_gui.common import get_save_file_name, open_file_name
from frame_up_gui.widgets import PreviewFrame

class CentralLayout(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout(self)
        layout.stretch(1)

        input_group = QtWidgets.QGroupBox("Select an Image Source")
        input_layout = QtWidgets.QHBoxLayout(input_group)

        input_widget = QtWidgets.QLineEdit("Hello from the input")
        input_widget.setReadOnly(True)

        @QtCore.Slot(str)
        def input_edit(path: str):
            ImagePathChanged.broadcast(path)
        input_widget.textChanged.connect(input_edit)

        @QtCore.Slot(str)
        def input_change(path: str):
            if path is not None and len(path) > 0:
                print("setting input to ", path)
                input_widget.setText(path)
            
        ImagePathChanged.listen(input_change)

        input_layout.addWidget(input_widget)

        input_button = QtWidgets.QPushButton("Browse...")
        input_button.setToolTip("Pick a local image to frame")

        @QtCore.Slot()
        def input_pushed():
            name, filters = open_file_name()
            print(f"ya imported {name}")
            ImagePathChanged.broadcast(name)
            # trigger load w/ image name
        input_button.clicked.connect(input_pushed)

        input_layout.addWidget(input_button, 0)
        layout.addWidget(input_group, 0)

        preview = PreviewFrame(title="Preview Image Frame")
        layout.addWidget(preview, 1)

        export_group = QtWidgets.QGroupBox("Save your framed image")
        export_layout = QtWidgets.QHBoxLayout(export_group)

        export_widget = QtWidgets.QLineEdit("<Suggested export path will appear here>")
        export_widget.setReadOnly(True)

        @QtCore.Slot(str)
        def export_edit(path: str):
            ExportPathChanged.broadcast(path)
        export_widget.textChanged.connect(export_edit)
        
        @QtCore.Slot(str)
        def export_change(path: str):
            export_widget.setText(path)
        ExportPathChanged.listen(export_change)

        @QtCore.Slot(str)
        def load_suggested(path: str):
            parsed_path = Path(path)
            suggested = get_suggested_filepath(parsed_path.parent, str(parsed_path.name))
            export_widget.setText(str(suggested))
        ImagePathChanged.listen(load_suggested)
        SaveCurrentImage.listen(load_suggested)

        # TODO: when the image is saved elsewhere, trigger a re-calc too


        export_layout.addWidget(export_widget, 1)

        # export_button = QtWidgets.QPushButton("Browse...")
        # @QtCore.Slot()
        # def export_pushed():
        #     name, filters = get_save_file_name()
        #     print(f"ya picked save path: {name}")
        #     ExportPathChanged.change(name)
        #     # trigger save w/ new file name
        # export_button.clicked.connect(export_pushed)
        # export_layout.addWidget(export_button, 0)

        save_button = QtWidgets.QPushButton("Save")
        save_button.setToolTip("Save to suggested file path")
        @QtCore.Slot()
        def save_pushed():
            # filename, filters = get_save_file_name()
            print(f"saving to suggested path {export_widget.text()}")
            # ExportPathChanged.change(name)
            # trigger save w/ new file name
            # save_to_disk(filename, )
            SaveCurrentImage.broadcast(export_widget.text())
            load_suggested(export_widget.text())
        save_button.clicked.connect(save_pushed)

        save_as_button = QtWidgets.QPushButton("Save as...")
        save_as_button.setToolTip("Save to another location")
        @QtCore.Slot()
        def save_as_pushed():
            filename, filters = get_save_file_name(export_widget.text())
            print(f"ya want to save to {filename}")
            # ExportPathChanged.change(name)
            # trigger save w/ new file name
            # save_to_disk(filename, )
            SaveCurrentImage.broadcast(filename)
        save_as_button.clicked.connect(save_as_pushed)

        export_layout.addWidget(save_button)
        export_layout.addWidget(save_as_button)

        layout.addWidget(export_group, 0)