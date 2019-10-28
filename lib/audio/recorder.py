from abc import ABC, abstractmethod
from pathlib import Path


class Recorder(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def record(self) -> Path:
        pass
