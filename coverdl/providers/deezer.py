import requests
from coverdl.providers.provider import Provider, Cover
from coverdl.providers.source import Source
from coverdl.exceptions import ProviderRequestFailed
from coverdl.utils import get_extension_from_url

class DeezerProvider(Provider):
    def __init__(self, base_url="https://api.deezer.com", source=Source.DEEZER):
        super().__init__(base_url, source)

    def get_covers(self, artist, album) -> list[Cover]:
        results = []
        params={
            "q": f"artist:\"{artist}\" album:\"{album}\""
        }
        r = requests.get(self.base_url + "/search/album", params=params)

        if r.ok:
            data = r.json()

            for item in data["data"]:
                results.append(
                    Cover(
                        artist=item["artist"]["name"],
                        title=item["title"],
                        source=self.source,
                        cover_url=item["cover_xl"],
                        ext=get_extension_from_url(item["cover_xl"])
                    )
                )
        else:
            raise ProviderRequestFailed(self.source, r.text)
        
        return results