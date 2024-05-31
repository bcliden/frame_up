from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget

range = (0, 100)


class IntensitySlider(QWidget):
    valueChanged = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #
        # widgets
        #

        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setTracking(False)
        slider.setRange(*range)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(5)
        slider.setValue(range[1])

        minimum = QLabel(str(range[0]))
        current = QLabel(str(range[1]))
        maximum = QLabel(str(range[1]))

        #
        # actions
        #

        slider.sliderMoved.connect(lambda i: current.move(i, current.y()))

        # tooltip values
        slider.setToolTip(str(range[1]))
        slider.sliderMoved.connect(lambda i: slider.setToolTip(str(i)))

        # pass value changes right through
        slider.valueChanged.connect(lambda v: self.valueChanged.emit(v))

        #
        # layout
        #

        layout = QHBoxLayout()
        layout.addWidget(minimum)
        layout.addWidget(slider)
        layout.addWidget(maximum)

        self.setLayout(layout)
