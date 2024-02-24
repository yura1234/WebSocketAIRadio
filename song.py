from dataclasses import dataclass

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
    byteArray : list()