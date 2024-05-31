from typing import Callable, Optional, Self

from frame_up.file import open_from_disk, save_to_disk
from frame_up.framing import frame_image
from frame_up.models import ImageEmailPayload
from frame_up.services import (
    antique_filter,
    email_image,
    monochrome_filter,
    vibrant_filter,
)
from PIL.Image import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPalette

from frame_up_gui.App import FrameUpApp
from frame_up_gui.events import EventBus as bus
from frame_up_gui.tasks import BackgroundTasker
from frame_up_gui.widgets.EmailDialog import EmailContactInfo

default_intensity = 100


def load_image_after(function: Callable):
    def wrapper(instance: "PreviewFrame", *args, **kwargs):
        value = function(instance, *args, **kwargs)
        instance.load_image()
        return value

    return wrapper


class PreviewFrame(QtWidgets.QLabel, BackgroundTasker):
    # Pillow Types
    original_image: Optional[Image]
    framed_image: Optional[Image]

    # QT Types
    qt_image: Optional[ImageQt]
    qt_pixmap: Optional[QtGui.QPixmap]
    scaled_pixmap: Optional[QtGui.QPixmap]

    # Canvas management
    # image_canvas: QtWidgets.QLabel
    image_min_height: int

    path: Optional[str]
    filter: Optional[str]
    intensity: Optional[int]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.original_image = None
        self.framed_image = None

        self.qt_image = None
        self.qt_pixmap = None
        self.scaled_pixmap = None

        self.image_min_height = 300

        self.path = None
        self.filter = None
        self.intensity = None

        # event connections
        bus.ImagePathChanged.connect(self.set_image_path)
        bus.SaveCurrentImage.connect(self.save_image)
        bus.EmailCurrentImage.connect(self.email_image)

        # TODO/bcl: should this just go in BackgroundTasker?
        FrameUpApp.instance().aboutToQuit.connect(self.clean_background_tasks)

        self.set_minimums(self.image_min_height)
        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.setAlignment(QtCore.Qt.AlignCenter)

        # self.setStyleSheet("border: 1px solid blue;")
        # self.image.setStyleSheet("border: 3px solid red;")

    #
    #   Event handler overrides
    #

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        # override of https://doc.qt.io/qt-6/qwidget.html#resizeEvent
        self.resize_image()

    def aspectRatio(self) -> float:
        pm = self.scaled_pixmap

        if pm is None:
            return 1.0

        width, height = pm.width(), pm.height()

        if width == 0 or height == 0:
            return 1.0

        return width / height

    #
    #   Slots
    #

    @QtCore.Slot(str)
    def save_image(self, filename) -> None:
        if self.qt_image is None:
            return
        save_to_disk(filename, self.qt_image)

    @QtCore.Slot(EmailContactInfo)
    def email_image(self: Self, info: EmailContactInfo) -> None:
        """Get contact info from user and send email payload to service"""

        image = self.framed_image
        if not image:
            return

        payload = ImageEmailPayload(to=info.to, subject_line=info.subject, data=image)
        self.send_task(
            email_image,
            payload,
            result_cb=lambda *a, **kw: print("result", *a, **kw),
            finished_cb=lambda *a, **kw: print("finished", *a, **kw),
        )

    @load_image_after
    @QtCore.Slot(str)
    def set_image_path(self, path: str) -> None:
        self.path = path

    @load_image_after
    @QtCore.Slot(str)
    def set_filter(self, value: str) -> None:
        if value.lower() == "none":
            self.filter = None
        else:
            self.filter = value

    @load_image_after
    @QtCore.Slot(int)
    def set_intensity(self, value: int) -> None:
        self.intensity = value

    def load_image(self) -> None:
        if self.path is None:
            print("can't load an image without a path.")
            return

        path = self.path
        filter = self.filter
        intensity = self.intensity or default_intensity

        intensity2: float = intensity / 100

        self.reset()

        self.original_image = open_from_disk(path)
        self.filtered_image = self.original_image

        match filter:
            case "Antique":
                self.filtered_image = antique_filter(self.original_image, intensity2)
            case "Vibrant":
                self.filtered_image = vibrant_filter(self.original_image, intensity2)
            case "Monochrome":
                self.filtered_image = monochrome_filter(self.original_image, intensity2)
            case None:
                pass
            case _:
                raise ValueError("Unknown filter: ", filter)

        self.framed_image = frame_image(self.filtered_image)

        self.qt_image = ImageQt(self.framed_image)
        self.qt_pixmap = QtGui.QPixmap.fromImage(self.qt_image)
        self.scaled_pixmap = self.qt_pixmap  # will be resized below

        self.resize_image()
        self.set_minimums(height=self.scaled_pixmap.height())

    def resize_image(self) -> None:
        if self.qt_pixmap is None:
            # print("no pixmap to resize. exiting")
            return

        geometry = self.geometry()
        # print(f"previewframe w={geometry.width()} h={geometry.height()}")
        self.scaled_pixmap = self.qt_pixmap.scaled(
            geometry.width(),
            geometry.height(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(self.scaled_pixmap)

    def set_minimums(self, height: Optional[int]):
        if height is None:
            height = self.image_min_height

        # or use whichever is longer?
        ratio = self.aspectRatio()

        height = max(height, self.image_min_height)
        width = round(height * ratio)

        self.setMinimumHeight(height)
        self.setMinimumWidth(width)

    def reset(self):
        self.original_image = None
        self.framed_image = None

        self.qt_image = None
        self.qt_pixmap = None
        self.scaled_pixmap = None
