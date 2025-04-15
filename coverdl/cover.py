from dataclasses import dataclass
from coverdl.providers.source import Source

@dataclass
class Cover:
    artist: str
    title: str
    source: Source
    cover_url: str
    ext: str
    confidence: int = 1
