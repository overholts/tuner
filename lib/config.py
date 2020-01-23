import sys
from datetime import timedelta
from pathlib import Path

import yaml

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
                    station=source["station"],
                    url=source["url"],
                    audio_format=source["format"],
                    start_time_cron=source["start_time_cron"],
                    duration=timedelta(minutes=source["duration_minutes"]),
                    path_template=__get_container_path_template(source),
                )
            )

    return Config(sources=sources)


def __get_container_path_template(source) -> Path:
    if Path(source["path_template"]).is_absolute():
        raise ValueError(
            (
                f"path_template for source {source['id']} ({source['name']}) must be relative! "
                "It will be rooted at the path mounted to '/output'."
            )
        )

    return Path("/output").joinpath(source["path_template"])


# for debugging purposes
if __name__ == "__main__":
    print(load_from_yaml(Path(sys.argv[1])))
