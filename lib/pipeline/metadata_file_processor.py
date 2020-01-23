import datetime
from abc import abstractmethod
from pathlib import Path
from typing import Dict

from lib.entities import Source
from lib.pipeline.file_processor import FileProcessor


class MetadataFileProcessor(FileProcessor):
    @abstractmethod
    def __init__(self, definition: Source, processed_dir: Path):
        super().__init__(processed_dir)
        self._definition = definition

    @abstractmethod
    def apply(self, input_file) -> Path:
        pass

    def _get_metadata_tags(self) -> Dict:
        # TODO Make this configurable
        return {
            "artist": self._definition.station,
            "album": "{} {}".format(self._definition.name, datetime.date.today().year),
            "title": "{} - {}".format(
                self._definition.name, datetime.date.today().strftime("%B %d, %Y")
            ),
            "track": self.__get_track_tag(),
        }

    @staticmethod
    def __get_track_tag() -> str:
        """
        Helper to compute the track position tag.

        TODO support this properly - probably parsing the cron to get:
          (occurrences thus far in ALBUM_PERIOD) / (total occurrences in ALBUM_PERIOD)
        :return:
        """

        return "1/1"
