import requests

def searchSong(name):
    url = "https://api.deezer.com/search"

    params = {
        "q": name,
        "limit": 1
    }

    r = requests.get(url, params=params)
    data = r.json()

    if not data["data"]:
        return None

    return data["data"][0]["link"]

