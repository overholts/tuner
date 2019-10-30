import logging
from datetime import timedelta, datetime
from pathlib import Path

import requests

from lib.audio.recorder import Recorder
from lib.files import filename

extension = "mp3"

logger = logging.getLogger("MP3Recorder")


class MP3Recorder(Recorder):
    def __init__(
        self, source_url: str, duration: timedelta, download_dir: Path, file_prefix: str
    ):
        super().__init__()
        self._source_url = source_url
        self._duration = duration
        self._download_dir = download_dir
        self._file_prefix = file_prefix

    def record(self) -> Path:
        end_time = datetime.now() + self._duration

        output_file = self._download_dir.joinpath(
            filename.get_temp_filename(self._file_prefix, extension)
        )

        stream_url = self._get_stream_url()
        logger.info(f"Recording for {self._duration} from {stream_url}")
        logger.debug(f"Recording to {output_file}")

        with requests.get(stream_url, stream=True) as res:
            res.raise_for_status()
            with open(str(output_file.absolute()), "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
                    if datetime.now() >= end_time:
                        logger.debug("Recording duration reached, closing stream.")
                        break

        logger.info(f"Done recording to {output_file}")
        return output_file

    def _get_stream_url(self):
        """
        Handle the most rudimentary of M3U playlists.
        :return: mp3 url
        """

        if self._source_url.split(".")[-1] == "m3u":
            logger.debug("Attempting to read m3u playlist.")
            with requests.get(self._source_url) as res:
                return res.text.splitlines()[0]
        else:
            return self._source_url
