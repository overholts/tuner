import logging
from abc import abstractmethod, ABC
from pathlib import Path
from typing import List

from apscheduler.triggers.base import BaseTrigger

from lib.environment import Environment
from lib.util.file_utils import remove

logger = logging.getLogger("Job")


class Job(ABC):
    @abstractmethod
    def __init__(self, job_id: int, env: Environment):
        self.id = job_id
        self.env = env

    @abstractmethod
    def run(self):
        """
        Concrete implementations should implement their desired functionality here.
        :return:
        """
        pass

    @abstractmethod
    def get_trigger(self) -> BaseTrigger:
        """
        Concrete implementations should implement an apscheduler trigger here.
        :return:
        """
        pass

    def _clean_intermediate_files(self, files: List[Path]):
        if not self.env.debug:
            for file in files:
                try:
                    remove(file)
                except OSError:
                    logger.warning(f"Failed to remove intermediate file {file}")
