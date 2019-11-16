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
    sources: List[Source]
