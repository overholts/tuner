from dataclasses import dataclass
from datetime import timedelta, tzinfo
from typing import List


@dataclass
class Source:
    id: int
    name: str
    url: str
    audio_format: str
    start_time_cron: str
    duration: timedelta


@dataclass
class Config:
    # When the user's time zone is not the same as the server where they run
    # the application, allow them to specify a time zone in the configuration
    # so they may specify show schedules in their local time.
    timezone: tzinfo
    sources: List[Source]
