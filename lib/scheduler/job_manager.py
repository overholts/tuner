import logging

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from lib.scheduler.job import Job

logger = logging.getLogger("JobManager")


class JobManager:
    def __init__(self, timezone):
        job_stores = {
            # Use our own persistence for jobs since we want to store additional metadata
            "default": MemoryJobStore()
        }

        executors = {
            # TODO Set this dynamically
            "default": ProcessPoolExecutor(4)
        }

        job_defaults = {"coalesce": False, "max_instances": 1}

        # BlockingScheduler doesn't handle SIGINT properly within Docker for some reason
        # Use BackgroundScheduler and do our own signal handling
        self._scheduler = BackgroundScheduler(
            jobstores=job_stores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=timezone,
        )

    def run(self):
        self._scheduler.start()

    def register(self, job: Job):
        self._scheduler.add_job(
            func=job.run,
            trigger=job.get_trigger(),
            id=str(job.id),
            max_instances=1,
            replace_existing=True,
        )

    def shutdown(self):
        logger.debug("Shutting down job manager.")
        self._scheduler.shutdown()
