from coverdl.exceptions import ProviderRequestFailed
from coverdl.providers.provider import Provider, Cover
from coverdl.providers.source import Source
import requests

class ITunesProvider(Provider):
    def __init__(self, base_url="https://itunes.apple.com", source=Source.ITUNES):
        super().__init__(base_url, source)

    def get_covers(self, artist, album, country='us'):
        results = []
        params = {
            "term": artist,
            "media": "music",
            "entity": "album"
        }
        r = requests.get(self.base_url + "/search", params=params)

        if r.ok:
            data = r.json()

            for item in data["results"]:
                if item["collectionName"].lower().strip() == album.lower().strip():
                    results.append(
                        Cover(
                            artist=item["artistName"],
                            title=item["collectionName"],
                            source=Source.ITUNES,
                            cover_url=item.get("artworkUrl100") or item.get("artworkUrl60")
                        )
                    )

            return results
        else:
            raise ProviderRequestFailed(self.source, r.text)