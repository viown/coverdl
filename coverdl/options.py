from dataclasses import dataclass
from coverdl.providers.source import Source

@dataclass
class Options:
    path: str
    providers: list[Source]
    cover_name: str
    tags: list[str]
    recursive: bool
    upgrade: bool
    max_size: float
    strict: bool
    no_silence_warnings: bool