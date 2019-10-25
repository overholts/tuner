import sys
from datetime import timedelta
from pathlib import Path

import yaml
from pytz import timezone

from lib.entities import Config, Source


def load_from_yaml(file: Path):
    sources = []
    with open(str(file.absolute()), "r") as config_file:
        raw_config = yaml.full_load(config_file.read())
        for index, source in enumerate(raw_config["sources"]):
            sources.append(
                Source(
                    id=source["id"],
                    name=source["name"],
                    url=source["url"],
                    audio_format=source["format"],
                    start_time_cron=source["start_time_cron"],
                    duration=timedelta(minutes=source["duration_minutes"]),
                )
            )

        tz = timezone(raw_config["timezone"])

    return Config(timezone=tz, sources=sources)


# for debugging purposes
if __name__ == "__main__":
    print(load_from_yaml(Path(sys.argv[1])))
