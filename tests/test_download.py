from coverdl.utils import download_cover
from coverdl.providers import AppleMusicProvider
import warnings
import os

def test_download(tmp_path):
    provider = AppleMusicProvider()

    covers = provider.get_covers("Dream Theater", "Train of Thought")

    if len(covers) > 0:
        download_cover(covers[0].cover_url, tmp_path, "default")

        assert os.path.exists(os.path.join(tmp_path, "default"))
    else:
        warnings.warn("AppleMusicProvider returned no results")
