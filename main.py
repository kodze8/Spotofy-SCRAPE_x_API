import spotipy
from spotipy.oauth2 import SpotifyOAuth
import song_search
import os

# Spotify App credentials

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
SCOPE = "playlist-modify-public"

ALBUM_NAME = "27th:04"

sp = None


def log_in():
    global sp
    scope = SCOPE
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
                                      scope=scope))
    except spotipy.SpotifyException:
        print("Problem with log in")


def create_playlist():
    global sp
    try:
        user_id = sp.me()["id"]
        sp.user_playlist_create(user_id, ALBUM_NAME, public=True)  # SUCCESFULLY ADDED
    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")


def find_playlist():
    global sp
    playlists = sp.current_user_playlists()
    try:
        where_to_add = [x["id"] for x in playlists["items"] if x["name"] == song_search.DATE][0]
        return where_to_add
    except IndexError:
        print("Playlist doesn't exit")


def add_songs():
    global sp
    log_in()
    create_playlist()
    playlist_uri = find_playlist()

    lst = song_search.top100_to_spotify_data()
    for x in lst:
        try:
            sp.playlist_add_items(playlist_uri, [x["uri"]])
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")


add_songs()
