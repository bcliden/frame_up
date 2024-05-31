from typing import Any, Callable, Optional

from PySide6.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    Signal,
    Slot,
)


class TaskSignals(QObject):
    """Because signals ONLY work on QObjects"""

    result = Signal(object)
    done = Signal()


class Task(QRunnable):
    """
    Can perform any action. Run this inside a thread pool with pool.start()
    """

    fn: Callable
    args: Any
    kwargs: Any
    signals: TaskSignals

    def __init__(self, fn: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self) -> None:
        result = None
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            print(e)  # nothing?
        self.signals.result.emit(result)
        self.signals.done.emit()


class BackgroundTasker:
    """
    Class mixin to do some work off the GUI thread

    don't forget to call `clean_background_tasks` when done!
    """

    pool = QThreadPool.globalInstance()

    def send_task(
        self,
        fn: Callable,
        *args,
        result_cb: Optional[Callable],
        finished_cb: Optional[Callable],
        **kwargs,
    ) -> None:
        print(f"creating task with fn={fn} args={args} kwargs={kwargs}")
        task = Task(fn, *args, **kwargs)
        worker_id = id(task)

        # Connect callbacks if specified
        if result_cb is not None:
            task.signals.result.connect(result_cb)
        if finished_cb is not None:
            task.signals.result.connect(finished_cb)

        # Debug callbacks
        task.signals.result.connect(
            lambda *a, **kw: self.log(f"[{worker_id} result]", *a, **kw)
        )
        task.signals.done.connect(
            lambda *a, **kw: self.log(f"[{worker_id} done]", *a, **kw)
        )

        self.pool.start(task)
        print(f"sent worker (id={worker_id}) to pool")

        # TODO/bcl can we even start and then hook up a signal?
        # return runnable

    def log(self, prefix, *args, **kwargs) -> None:
        print(prefix, args, kwargs)

    @Slot()
    def clean_background_tasks(self):
        print(f"waiting for {self.pool.activeThreadCount()} b.g. tasks to finish?")
        # success = self.pool.waitForDone(200)
        success = self.pool.waitForDone(-1)  # is this a problem? wait forever
        if success:
            print("thread pool closed cleanly")
        else:
            print("thread pool closed messily :(")
