from abc import ABCMeta, abstractmethod
from .RoutineState import Result


class IRoutine(metaclass=ABCMeta):
    @abstractmethod
    def start(self, *args, **kwargs) -> Result:
        pass

    @abstractmethod
    def monitor(self) -> Result:
        pass

    @abstractmethod
    def abort(self):
        pass
