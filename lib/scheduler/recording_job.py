import logging
from pathlib import Path

import inflection

from lib.audio.mp3_recorder import MP3Recorder
from lib.entities import Source
from lib.scheduler.cron_job import CronJob

logger = logging.getLogger("RecordingJob")


class RecordingJob(CronJob):
    def __init__(self, definition: Source, download_dir: Path):
        super().__init__(definition.id, definition.start_time_cron)
        self._duration = definition.duration
        self._url = definition.url
        self._download_dir = download_dir
        self._file_prefix = self._get_file_prefix(definition)

        # TODO select from factory by Source audio format.
        self._recorder = MP3Recorder(
            self._url, self._duration, self._download_dir, self._file_prefix
        )

    def run(self):
        logger.info(f"Recording for {self._duration}")

        self._recorder.record()
        # TODO process output file and store to library

        logger.info(f"Done recording")

    @staticmethod
    def _get_file_prefix(definition: Source):
        return "{}_{}".format(
            definition.id, inflection.underscore(definition.name).replace(" ", "_")
        )
