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

    @abstractmethod
    def get_covers(self, artist: str, album: str, country: str) -> list[Cover]:
        pass