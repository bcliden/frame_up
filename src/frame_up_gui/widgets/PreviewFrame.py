from typing import Optional, Self

from frame_up.file import open_from_disk, save_to_disk
from frame_up.framing import frame_image
from frame_up.models import ImageEmailPayload
from frame_up.services import email_image
from PIL.Image import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPalette

from frame_up_gui.App import FrameUpApp
from frame_up_gui.events import EmailCurrentImage, ImagePathChanged, SaveCurrentImage
from frame_up_gui.tasks import BackgroundTasker
from frame_up_gui.widgets.EmailDialog import EmailContactInfo


class PreviewFrame(QtWidgets.QGroupBox, BackgroundTasker):
    # Pillow Types
    original_image: Image | None
    framed_image: Image | None

    # QT Types
    qt_image: ImageQt | None
    qt_pixmap: QtGui.QPixmap | None
    scaled_pixmap: QtGui.QPixmap | None

    # Canvas management
    image_canvas: QtWidgets.QLabel
    image_min_height: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.original_image = None
        self.framed_image = None

        self.qt_image = None
        self.qt_pixmap = None
        self.scaled_pixmap = None

        self.image_min_height = 300

        # event connections
        ImagePathChanged.listen(self.load_file)
        SaveCurrentImage.listen(self.save_image)
        EmailCurrentImage.listen(self.email_image)
        FrameUpApp.instance().aboutToQuit.connect(self.clean_background_tasks)

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
        new_height = int(self.aspectRatio() * hint.height())
        hint.setHeight(new_height)
        # print(f"pf.sizeHint -> {hint}")
        return hint

    def aspectRatio(self) -> float:
        pm = self.scaled_pixmap

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

    def resizeImage(self) -> None:
        if self.qt_pixmap is None:
            print("no pixmap to resize. exiting")
            return

        geometry = self.image_canvas.geometry()
        self.scaled_pixmap = self.qt_pixmap.scaled(
            geometry.width(),
            geometry.height(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.image_canvas.setPixmap(self.scaled_pixmap)

    @QtCore.Slot(str)
    def load_file(self, path: str) -> None:
        # if self.scaled_pixmap is None:
        #     return

        self.reset()

        self.original_image = open_from_disk(path)
        self.framed_image = frame_image(self.original_image)

        self.qt_image = ImageQt(self.framed_image)
        self.qt_pixmap = QtGui.QPixmap.fromImage(self.qt_image)
        self.scaled_pixmap = self.qt_pixmap  # will be resized below

        self.resizeImage()
        self.setMinimums(height=self.scaled_pixmap.height())

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

    def setMinimums(self, height: Optional[int]):
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
