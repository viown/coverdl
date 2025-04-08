import requests
import os
import mimetypes

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

def download_cover(url, target, cover_name):
    type = mimetypes.guess_type(url)[0]
    ext = mimetypes.guess_extension(type)

    r = requests.get(url)
    r.raise_for_status()

    with open(os.path.join(target, cover_name + ext), 'wb') as f:
        f.write(r.content)

def get_recursive_paths(path):
    paths = []
    for artist_path in os.listdir(path):
        for album_path in os.listdir(os.path.join(path, artist_path)):
            album_path = os.path.join(path, artist_path, album_path)
            if os.path.isdir(album_path):
                paths.append(album_path)
    return paths

def get_base_path(path):
    if os.path.isfile(path):
        return os.path.dirname(path)
    return os.path.normpath(path)

def has_cover(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)

    files = os.listdir(path)

    for file in files:
        name, ext = os.path.splitext(file)
        if ext in IMAGE_EXTENSIONS and name in ["folder", "poster", "cover", "default"]:
            return True
    return False