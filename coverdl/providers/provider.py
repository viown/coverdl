from abc import ABC, abstractmethod
from coverdl.providers.source import Source
from dataclasses import dataclass

@dataclass
class Cover:
    artist: str
    title: str
    source: Source
    cover_url: str
    ext: str
    confidence: int = 1

class Provider(ABC):
    BASE_URL: str | None
    SOURCE: Source

    @abstractmethod
    def get_covers(self, artist: str, album: str) -> list[Cover]:
        pass