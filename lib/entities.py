from dataclasses import dataclass
from datetime import timedelta
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
    timezone: str
    sources: List[Source]
