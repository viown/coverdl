from coverdl.exceptions import ProviderRequestFailed
from coverdl.providers.provider import Provider, Cover
from coverdl.providers.source import Source
from coverdl.utils import get_extension_from_url
from difflib import SequenceMatcher
import requests

class ITunesProvider(Provider):
    BASE_URL = "https://itunes.apple.com"
    SOURCE = Source.ITUNES

    def get_covers(self, artist, album):
        results = []
        params = {
            "term": artist,
            "media": "music",
            "entity": "album"
        }
        r = requests.get(self.BASE_URL + "/search", params=params, timeout=10)

        if r.ok:
            data = r.json()

            for item in data["results"]:
                # Check if the album names are somewhat similar.
                # TODO: Filter out possible identifiers in the name
                similarity_ratio = SequenceMatcher(None, item["collectionName"].lower().strip(), album.lower().strip()).ratio()
                if similarity_ratio > 0.8:
                    cover_url = item.get("artworkUrl100") or item.get("artworkUrl60")
                    results.append(
                        Cover(
                            artist=item["artistName"],
                            title=item["collectionName"],
                            source=self.SOURCE,
                            cover_url=cover_url,
                            confidence=similarity_ratio,
                            ext=get_extension_from_url(cover_url)
                        )
                    )

            return sorted(results, key=lambda c: c.confidence, reverse=True)
        raise ProviderRequestFailed(self.SOURCE, r.text)