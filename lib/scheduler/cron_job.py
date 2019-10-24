import logging
from abc import abstractmethod

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger

from lib.scheduler.job import Job

logger = logging.getLogger("CronJob")


class CronJob(Job):
    """
    Abstract Job which uses cron trigger for scheduling.
    """

    @abstractmethod
    def __init__(self, job_id: int, cron_expression: str):
        super().__init__(job_id)
        self.__cron_expression = cron_expression

    def get_trigger(self) -> BaseTrigger:
        cron_fields = self.__cron_expression.split()

        logger.debug(f"Parsed cron fields {cron_fields}")
        return CronTrigger(
            day_of_week=cron_fields[4],
            month=cron_fields[3],
            day=cron_fields[2],
            hour=cron_fields[1],
            minute=cron_fields[0],
        )

    @abstractmethod
    def run(self):
        """
        Concrete implementations should implement their desired functionality here.
        :return:
        """
        pass
