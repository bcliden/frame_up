from abc import abstractmethod
from typing import Any, Protocol, TypeVar, Generic
from PySide6.QtCore import QObject, Signal, SignalInstance

T = TypeVar("T")
class SignalTower(Generic[T]):
    name: str
    type: type
    _evt: SignalInstance

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        cls._evt = Signal(cls.type, name=cls.__name__)

    def listen(self, fn) -> SignalInstance:
        return self._evt.connect(fn)

    def change(self, message: T):
        self._evt.emit(message)


class _ImagePathChanged(QObject, SignalTower[str]):
    type = str

ImagePathChanged = _ImagePathChanged()


class _ExportPathChanged(QObject, SignalTower[str]):
    type = str

ExportPathChanged = _ExportPathChanged()