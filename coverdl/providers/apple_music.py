from coverdl.providers.provider import Provider
from coverdl.providers.itunes import ITunesProvider
from coverdl.providers.source import Source

class AppleMusicProvider(ITunesProvider):
    def __init__(self, base_url="https://itunes.apple.com", source=Source.APPLE_MUSIC):
        super().__init__(base_url, source)

    def _transform_url(self, itunes_url, country='us'):
        cover_url = itunes_url.replace("is1-ssl", "a1")
        cover_url = cover_url.replace("/image/", f"/{country}/")
        cover_url = cover_url.replace("/thumb/", "/r1000/063/")

        cover_url = '/'.join(cover_url.split('/')[:-1])

        return cover_url

    def get_covers(self, artist, album, country='us'):
        covers = super().get_covers(artist, album, country)

        for cover in covers:
            cover.cover_url = self._transform_url(cover.cover_url, country)

        return covers