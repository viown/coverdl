from coverdl.providers.provider import Provider
from coverdl.providers.itunes import ITunesProvider
from coverdl.providers.source import Source

class AppleMusicProvider(ITunesProvider):
    def __init__(self):
        self.base_url = "https://itunes.apple.com"
        self.source = Source.APPLE_MUSIC

    def _transform_url(self, itunes_url, country='us'):
        itunes_url = itunes_url.replace("is1-ssl", "a1")
        itunes_url = itunes_url.replace("/image/", f"/{country}/")
        itunes_url = itunes_url.replace("/thumb/", "/r1000/063/")

        itunes_url = '/'.join(itunes_url.split('/')[:-1])

        return itunes_url

    def get_covers(self, artist, album, country='us'):
        covers = super().get_covers(artist, album, country)

        for cover in covers:
            cover.source = Source.APPLE_MUSIC
            cover.cover_url = self._transform_url(cover.cover_url)

        return covers