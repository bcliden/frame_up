from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette

from frame_up_gui.events import ImagePathChanged, ExportPathChanged
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
        input_widget.setDisabled(True)

        @QtCore.Slot(str)
        def input_edit(path: str):
            ImagePathChanged.change(path)
        input_widget.textChanged.connect(input_edit)

        @QtCore.Slot(str)
        def input_change(path: str):
            input_widget.setText(path)
        ImagePathChanged.listen(input_change)

        input_layout.addWidget(input_widget)

        input_button = QtWidgets.QPushButton("Browse...")

        @QtCore.Slot()
        def input_pushed():
            name, filters = open_file_name()
            print(f"ya imported {name}")
            ImagePathChanged.change(name)
            # trigger load w/ image name
        input_button.clicked.connect(input_pushed)

        input_layout.addWidget(input_button, 0)
        layout.addWidget(input_group, 0)

        preview = PreviewFrame(title="Preview Image Frame")
        layout.addWidget(preview, 1)

        export_group = QtWidgets.QGroupBox("Export your framed image")
        export_layout = QtWidgets.QHBoxLayout(export_group)

        export_widget = QtWidgets.QLineEdit("Hello from export")
        export_widget.setDisabled(True)

        @QtCore.Slot(str)
        def export_edit(path: str):
            ExportPathChanged.change(path)
        export_widget.textChanged.connect(export_edit)
        
        @QtCore.Slot(str)
        def export_change(path: str):
            print("[exp ch]", path)
            export_widget.setText(path)
        ExportPathChanged.listen(export_change)

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
        @QtCore.Slot()
        def save_pushed():
            name, filters = get_save_file_name()
            print(f"ya want to save to {name}")
            # ExportPathChanged.change(name)
            # trigger save w/ new file name
        save_button.clicked.connect(save_pushed)

        export_layout.addWidget(save_button, 0)
    
        layout.addWidget(export_group, 0)
