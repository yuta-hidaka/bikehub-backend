
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import requests


def get_remote_image(img_url):
    try:
        res = requests.get(img_url)
        res.raise_for_status()
    except Exception:
        return None

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(img_url).read())
    img_temp.flush()

    return img_temp
