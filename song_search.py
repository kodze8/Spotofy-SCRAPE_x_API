import base64
import requests
import top_100
import os


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
ACCESS_TOKEN = None
DATE = "2004-05-29"


def __get_token_access():
    search_endpoint = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
    }
    response = requests.post(search_endpoint, data=data, headers=headers)
    token_data = response.json()["access_token"]
    return token_data


ACCESS_TOKEN = __get_token_access()


def get_track(song_name, artist):
    global ACCESS_TOKEN
    search_endpoint = "https://api.spotify.com/v1/search"
    param = {
        "q": f"track:{song_name} artist:{artist}",
        "type": "track",
        "limit": 5
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(search_endpoint, params=param, headers=headers).json()
    return response


def filtered_rack_into_dict(song_name, artist):
    tracks = get_track(song_name, artist)
    # with open("temp.json", 'w') as file:
    #     json.dump(tracks, file, indent=4)

    lst = tracks["tracks"]["items"]
    key_list = ["album", "artists", "name", "id", "uri"]
    aat = [({k: (v["name"] if k == "album" else v[0]["name"] if k == "artists" else v) for k, v in x.items() if
             key_list.__contains__(k)}) for x in lst]

    if len(aat) != 0:
        return aat[0]
    return None


def top100_to_spotify_data():
    songs = []
    song_author = top_100.song_author_pair(DATE)
    for (x, y) in song_author:
        songs.append(filtered_rack_into_dict(x, y))
    return list(filter(lambda a: a is not None, songs))
