from coverdl.providers.provider import Provider
from coverdl.providers.itunes import ITunesProvider
from coverdl.providers.source import Source
from coverdl.utils import get_extension_from_url
import requests

class AppleMusicProvider(ITunesProvider):
    def __init__(self):
        super().__init__(Source.APPLE_MUSIC)

    def _transform_url(self, itunes_url, country='us'):
        # Convert the iTunes url into a higher-quality Apple Music equivalent
        cover_url = itunes_url.replace("is1-ssl", "a1")
        cover_url = cover_url.replace("/image/", f"/{country}/")
        cover_url = cover_url.replace("/thumb/", "/r1000/063/")

        cover_url = '/'.join(cover_url.split('/')[:-1])

        return cover_url
    
    def _test_url(self, url):
        r = requests.head(url)

        return r.ok

    def get_covers(self, artist, album, country='us'):
        results = []
        covers = super().get_covers(artist, album, country)

        for cover in covers:
            cover.cover_url = self._transform_url(cover.cover_url, country)
            cover.ext = get_extension_from_url(cover.cover_url)
            if self._test_url(cover.cover_url):
                results.append(cover)

        return results