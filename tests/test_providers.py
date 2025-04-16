from click.testing import CliRunner
from coverdl.providers import (
    AppleMusicProvider,
    DeezerProvider,
    DiscogsProvider,
    ITunesProvider
)
import shutil
import os

def test_apple_music():
    provider = AppleMusicProvider()

    provider.get_covers("Artist", "Album")

def test_deezer_provider():
    provider = DeezerProvider()

    provider.get_covers("Artist", "Album")

def test_discogs_provider():
    provider = DiscogsProvider()

    provider.get_covers("Artist", "Album")

def test_itunes_provider():
    provider = ITunesProvider()

    provider.get_covers("Artist", "Album")
