from .source import Source
from .provider import Provider
from .deezer import DeezerProvider
from .itunes import ITunesProvider
from .apple_music import AppleMusicProvider

providers: list[Provider] = [
    DeezerProvider(),
    ITunesProvider(),
    AppleMusicProvider()
]