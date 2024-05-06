from typing import Optional
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette
from PIL.Image import Image
from PIL.ImageQt import ImageQt

from frame_up.file import open_from_disk
from frame_up.framing import frame_image
from frame_up_gui.events import ImagePathChanged, ExportPathChanged
from frame_up_gui.common import get_save_file_name, open_file_name


class PreviewFrame(QtWidgets.QGroupBox):
    core_image: ImageQt | None
    shown_pixmap: QtGui.QPixmap | None
    image_canvas: QtWidgets.QLabel
    image_min_height: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.core_image = None
        self.shown_pixmap = None
        self.image_min_height = 300

        # event connections
        ImagePathChanged.listen(self.load_file)

        self.setMinimums(self.image_min_height)

        layout = QtWidgets.QVBoxLayout(self)
        # layout.setAlignment(QtCore.Qt.AlignCenter)

        image = QtWidgets.QLabel(self)
        # image.setScaledContents(True)
        image.setBackgroundRole(QPalette.ColorRole.Base)
        image.setAlignment(QtCore.Qt.AlignCenter)
        image.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored,
            QtWidgets.QSizePolicy.Policy.Ignored,
        )
        self.image_canvas = image
        # add to directory?
        layout.addWidget(self.image_canvas)

        # self.setStyleSheet("border: 1px solid blue;")
        # self.image.setStyleSheet("border: 3px solid red;")

    def sizeHint(self) -> QtCore.QSize:
        # override of: https://doc.qt.io/qt-6/qwidget.html#sizeHint-prop
        hint = super().sizeHint()
        # print(f"[pf.sizeHint original] = {hint}")
        hint.setHeight(self.aspectRatio() * hint.height())
        # print(f"pf.sizeHint -> {hint}")
        return hint

    def aspectRatio(self) -> float:
        pm = self.shown_pixmap

        # if not self.image.isVisible():
        #     print("[no viz] using default aspect ratio of 1.0")
        #     return 1.0

        if pm is None:
            # print("[no pm ] using default aspect ratio of 1.0")
            return 1.0

        width, height = pm.width(), pm.height()

        if width == 0 or height == 0:
            # print("[no w/h] using default aspect ratio of 1.0")
            return 1.0

        ar = width / height
        # print(f"aspect ratio for image is {pm.width()} / {pm.height()} = {ar} ")
        return ar

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        # override of https://doc.qt.io/qt-6/qwidget.html#resizeEvent
        # return super().resizeEvent(event)
        self.resizeImage()

    def resizeImage(self):
        if self.core_image is None:
            print("no pixmap to resize. exiting")
            return

        _, _, width, height = self.image_canvas.geometry().getRect()
        pm = QtGui.QPixmap.fromImage(self.core_image)
        self.shown_pixmap = pm.scaled(
            width,
            height,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.image_canvas.setPixmap(self.shown_pixmap)

    @QtCore.Slot(str)
    def load_file(self, path):
        # self.image.hide()
        # self.load_image(path)
        image = open_from_disk(path)
        image = frame_image(image)
        self.core_image = ImageQt(image)

        # or QImageReader?
        # pixmap = QtGui.QPixmap.fromImage(self.core_image)
        # success = pixmap.load(path)

        # if success is False:
        #     print(f"uh oh, couldn't load image: {path}")
        #     return

        # self.core_image = pixmap
        self.resizeImage()
        # self.image.show()

        self.setMinimums(height=self.shown_pixmap.height())

    def load_img(self, img: Image):
        self.core_image = ImageQt(img)
        self.resizeImage()

    def setMinimums(self, height: Optional[int]):
        if height is None:
            height = self.image_min_height

        # or use whichever is longer?
        ratio = self.aspectRatio()

        height = max(height, self.image_min_height)

        print(f"setting min={height} and max={height * ratio}")
        self.setMinimumHeight(height)
        self.setMinimumWidth(height * ratio)
