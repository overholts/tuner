import logging
from datetime import datetime
from pathlib import Path

import inflection

from lib.audio.mp3_recorder import MP3Recorder
from lib.entities import Source
from lib.environment import Environment
from lib.library.file_store import FileStore
from lib.pipeline.ffmpeg_file_processor import FFMpegFileProcessor
from lib.scheduler.cron_job import CronJob

logger = logging.getLogger("RecordingJob")


class RecordingJob(CronJob):
    def __init__(
        self,
        definition: Source,
        download_dir: Path,
        processed_dir: Path,
        env: Environment,
    ):
        super().__init__(definition.id, definition.start_time_cron, env)
        self._duration = definition.duration
        self._url = definition.url
        self._download_dir = download_dir
        self._file_prefix = self._get_file_prefix(definition)

        # TODO select from factory by Source audio format.
        self._recorder = MP3Recorder(
            self._url, self._duration, self._download_dir, self._file_prefix
        )

        self._file_processor = FFMpegFileProcessor(definition, processed_dir)

        self._file_store = FileStore(definition)

    def run(self):
        logger.info(f"Running recording job with id {self.id}")

        air_date = datetime.now()
        downloaded_file = self._recorder.record()

        processed_file = self._file_processor.apply(downloaded_file)

        self._file_store.put(processed_file, air_date)

        self._clean_intermediate_files([downloaded_file, processed_file])

    @staticmethod
    def _get_file_prefix(definition: Source):
        return "{}_{}".format(
            definition.id, inflection.underscore(definition.name).replace(" ", "_")
        )
