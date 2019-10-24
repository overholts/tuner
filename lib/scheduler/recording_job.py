import logging

from lib.entities import Source
from lib.scheduler.cron_job import CronJob

logger = logging.getLogger("RecordingJob")


class RecordingJob(CronJob):
    def __init__(self, definition: Source):
        super().__init__(definition.id, definition.start_time_cron)
        self._duration_minutes = definition.duration_minutes
        self._url = definition.url

    def run(self):
        logger.info(f"Recording for {self._duration_minutes} minutes")

        # TODO record from audio stream to configured destination

        logger.info(f"Done recording")
