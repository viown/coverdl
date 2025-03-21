import requests
from coverdl.providers.provider import Provider, Cover
from coverdl.providers.source import Source
from coverdl.exceptions import ProviderRequestFailed

class DeezerProvider(Provider):
    def __init__(self):
        super().__init__("https://api.deezer.com", Source.DEEZER)

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
                        source=Source.DEEZER,
                        cover_url=item["cover_xl"]
                    )
                )
        else:
            raise ProviderRequestFailed(r.text)
        
        return results