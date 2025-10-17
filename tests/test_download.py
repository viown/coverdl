from coverdl.providers import AppleMusicProvider
import warnings
import os

def test_download(tmp_path):
    provider = AppleMusicProvider()

    covers = provider.get_covers("System of a Down", "Toxicity")

    if len(covers) > 0:
        covers[0].download(os.path.join(tmp_path, "default"))

        assert os.path.exists(os.path.join(tmp_path, "default"))
    else:
        warnings.warn("AppleMusicProvider returned no results")
