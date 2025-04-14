from .provider import Provider
from .deezer import DeezerProvider
from .itunes import ITunesProvider
from .apple_music import AppleMusicProvider
from .discogs import DiscogsProvider

providers: list[Provider] = [
    DeezerProvider(),
    ITunesProvider(),
    AppleMusicProvider(),
    DiscogsProvider()
]