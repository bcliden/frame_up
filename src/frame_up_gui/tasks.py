from typing import Any, Self

from PySide6.QtCore import QObject, QThread, Signal, SignalInstance, Slot

"""
We don't really need all of these signals, I think?
can probably use the builtin thread signals
"""


class Signals(QObject):
    success = Signal(Any)
    failure = Signal(str)


class OffThread(QThread):
    """
    Any action, run this inside a thread pool with pool.start()
    """

    def __init__(self, fn, *args, **kwargs) -> Self:
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    def run(self: Self) -> None:
        print("OffThread task is starting: ", self)
        try:
            result = self.fn(*self.args, **self.kwargs)
            print("OffThread result is = ", result)
            self.signals.success.emit(result)
        except Exception as e:
            print("OffThread failed with exc = ", str(e))
            self.signals.failure.emit(str(e))
        print("OffThread task is done.")
        self.deleteLater()
