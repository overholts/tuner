import logging
import subprocess
from pathlib import Path

from lib.entities import Source
from lib.pipeline.metadata_file_processor import MetadataFileProcessor

logger = logging.getLogger("FFMpegFileProcessor")


class FFMpegFileProcessor(MetadataFileProcessor):
    def __init__(self, definition: Source, processed_dir: Path):
        super().__init__(definition, processed_dir)

    def apply(self, input_file: Path) -> Path:
        logger.info(f"Processing file {input_file}")
        metadata = []
        for key, value in self._get_metadata_tags().items():
            metadata.extend(["-metadata", f"{key}={value}"])

        output_file = self._processed_dir.joinpath(input_file.name)

        command = [
            "ffmpeg",
            "-i",
            str(input_file),
            "-t",
            str(self._definition.duration.seconds),
            "-c",
            "copy",
        ]
        command.extend(metadata)
        command.append(str(output_file))

        logger.debug("Executing: '{}'".format(" ".join(command)))
        subprocess.check_output(command)

        logger.info(f"Processed output file {output_file}")
        return output_file
