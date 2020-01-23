import os
import shutil
from pathlib import Path


def copy(source: Path, destination: Path):
    os.makedirs(destination.parent, 0o755, exist_ok=True)
    shutil.copy(str(source), str(destination))


def remove(target: Path):
    os.remove(target)
