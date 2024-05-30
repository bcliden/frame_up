from PySide6.QtCore import QRunnable, Slot


class OffThread(QRunnable):
    """
    Any action, run this inside a thread pool with pool.start()
    """

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @Slot(None)
    def run(self):
        self.fn(*self.args, **self.kwargs)
