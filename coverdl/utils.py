import requests
import os

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

def download_url(url, target):
    pass

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