from abc import ABC, abstractmethod
from coverdl.providers.source import Source
from dataclasses import dataclass

@dataclass
class Cover:
    artist: str
    title: str
    source: Source
    cover_url: str

class Provider(ABC):
    base_url: str
    source: Source

    def __init__(self, base_url: str, source: Source):
        self.base_url = base_url
        self.source = source

    @abstractmethod
    def get_covers(self, artist: str, album: str, country: str) -> list[Cover]:
        pass