from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QComboBox, QFormLayout, QGroupBox, QSizePolicy

from frame_up_gui.widgets.IntensitySlider import IntensitySlider
from frame_up_gui.widgets.PreviewFrame import PreviewFrame

filter_names = ["None", "Antique", "Vibrant", "Monochrome"]


class PreviewLayout(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Widgets

        frame = PreviewFrame()
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        filter = QComboBox()
        filter.addItems(filter_names)

        intensity = IntensitySlider()

        # Actions
        filter.currentTextChanged.connect(frame.set_filter)
        intensity.valueChanged.connect(frame.set_intensity)

        # Layout

        layout = QFormLayout()
        layout.addRow("Filter", filter)
        layout.addRow("Intensity", intensity)
        layout.addRow(frame)
        # layout.addWidget(frame)
        self.setLayout(layout)

    @Slot()
    def filter_image(self): ...

    @Slot()
    def debounced_filter_image(self): ...
