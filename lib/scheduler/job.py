import logging
from abc import abstractmethod, ABC

from apscheduler.triggers.base import BaseTrigger

logger = logging.getLogger("Job")


class Job(ABC):
    @abstractmethod
    def __init__(self, job_id: int):
        self.id = job_id

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
