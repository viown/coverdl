from PIL import Image
import requests
import os
import mimetypes
import imagehash
from coverdl.metadata import SUPPORTED_SONG_EXTENSIONS

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

def download_cover(url, target, cover_name):
    mimetype = mimetypes.guess_type(url)[0]
    ext = mimetypes.guess_extension(mimetype)

    r = requests.get(url, timeout=10)
    r.raise_for_status()

    with open(os.path.join(target, cover_name + ext), 'wb') as f:
        f.write(r.content)

def compare_covers(img1, img2):
    hash_0 = imagehash.average_hash(Image.open(img1))
    hash_1 = imagehash.average_hash(Image.open(img2))

    return hash_0 - hash_1

def get_paths_with_covers(path):
    paths = []
    for root, dirs, _ in os.walk(path):
        for current_dir in dirs:
            full_dir = os.path.join(root, current_dir)
            if is_album_dir(full_dir):
                paths.append(full_dir)
    return paths

def get_base_path(path):
    if os.path.isfile(path):
        return os.path.dirname(path)
    return os.path.normpath(path)

def get_cover(path):
    if os.path.isfile(path):
        path = os.path.dirname(os.path.abspath(path))

    files = os.listdir(path)

    for file in files:
        name, ext = os.path.splitext(file)
        if ext in IMAGE_EXTENSIONS and name in ["folder", "poster", "cover", "default"]:
            return os.path.join(path, file)

def has_song(dir):
    for f in os.listdir(dir):
        _, ext = os.path.splitext(f)
        if ext in SUPPORTED_SONG_EXTENSIONS:
            return True
    return False

def has_cover(path):
    return bool(get_cover(path))

def is_album_dir(dir):
    return has_cover(dir) and has_song(dir)