from dataclasses import dataclass
from typing import List

@dataclass
class Song:
    artist: str
    name: str
    year: int
    style: str
    # size: int
    duration: tuple
    # durationText: str
    summary: str
    byteArray : List