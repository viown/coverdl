from abc import ABC, abstractmethod
from coverdl.providers.source import Source
from coverdl.cover import Cover

class Provider(ABC):
    BASE_URL: str | None
    SOURCE: Source

    @abstractmethod
    def get_covers(self, artist: str, album: str) -> list[Cover]:
        pass