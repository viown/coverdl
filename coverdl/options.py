from dataclasses import dataclass
from coverdl.providers.source import Source

@dataclass
class Options:
    path: tuple[str]
    providers: tuple[Source]
    cover_name: str
    cache: str
    tags: tuple[str]
    recursive: bool
    upgrade: bool
    max_size: float
    max_upgrade_size: float
    strict: bool
    max_hamming_distance: int
    silence_warnings: bool
    delete_old_covers: bool