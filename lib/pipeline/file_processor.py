from abc import ABC, abstractmethod
from pathlib import Path


class FileProcessor(ABC):
    @abstractmethod
    def __init__(self, processed_dir: Path):
        self._processed_dir = processed_dir

    @abstractmethod
    def apply(self, input_file) -> Path:
        pass
