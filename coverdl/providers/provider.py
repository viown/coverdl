from typing import Optional
from abc import ABC, abstractmethod
from coverdl.providers.source import Source
from coverdl.cover import ExtCover
from difflib import SequenceMatcher

class Provider(ABC):
    BASE_URL: Optional[str] = None
    SOURCE: Source
    API_KEY: Optional[str] = None
    SECRET_KEY: Optional[str] = None

    def compare_titles(self, title1: str, title2: str) -> float:
        return SequenceMatcher(None, title1.lower().strip(), title2.lower().strip()).ratio()

    @abstractmethod
    def get_covers(self, artist: str, album: str) -> list[ExtCover]:
        pass
