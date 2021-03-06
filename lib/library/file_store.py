import logging
from datetime import datetime
from pathlib import Path

from lib.entities import Source
from lib.library.datetime_path_resolver import DatetimePathResolver
from lib.util.file_utils import copy
from lib.library.parameterized_path_resolver import ParameterizedPathResolver

logger = logging.getLogger("FileStore")


class FileStore:
    def __init__(self, definition: Source):
        self._definition = definition

        self._path_resolver = DatetimePathResolver(
            ParameterizedPathResolver(definition.path_template)
        )

    def put(self, file: Path, time: datetime):
        destination = self._path_resolver.get_path(time)

        if not destination.suffix == self._definition.audio_format:
            destination = destination.with_suffix(
                destination.suffix + "." + self._definition.audio_format
            )

        logger.info(f"Storing recording to {destination}")
        copy(file, destination)
