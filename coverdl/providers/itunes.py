from coverdl.exceptions import ProviderRequestFailed
from coverdl.providers.provider import Provider, Cover
from coverdl.providers.source import Source
from difflib import SequenceMatcher
import requests

class ITunesProvider(Provider):
    def __init__(self, source=Source.ITUNES):
        super().__init__("https://itunes.apple.com", source)

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
                # Check if the album names are somewhat similar.
                # TODO: Filter out possible identifiers in the name
                similarity_ratio = SequenceMatcher(None, item["collectionName"].lower().strip(), album.lower().strip()).ratio()
                if similarity_ratio > 0.8:
                    results.append(
                        Cover(
                            artist=item["artistName"],
                            title=item["collectionName"],
                            source=self.source,
                            cover_url=item.get("artworkUrl100") or item.get("artworkUrl60"),
                            confidence=similarity_ratio
                        )
                    )

            return sorted(results, key=lambda c: c.confidence, reverse=True)
        else:
            raise ProviderRequestFailed(self.source, r.text)