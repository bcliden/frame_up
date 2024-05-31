from PySide6.QtCore import QObject, Signal

from frame_up_gui.widgets.EmailDialog import EmailContactInfo


class _EventBus(QObject):
    ImagePathChanged = Signal(str)
    ExportPathChanged = Signal(str)
    SaveCurrentImage = Signal(str)
    EmailCurrentImage = Signal(EmailContactInfo)


EventBus = _EventBus()
