from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import List


@dataclass
class Source:
    id: int
    name: str
    station: str
    url: str
    audio_format: str
    start_time_cron: str
    duration: timedelta
    path_template: Path


@dataclass
class Config:
    sources: List[Source]
