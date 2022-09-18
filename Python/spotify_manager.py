# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
import spotipy, sys, pprint, json

class SpotifyManager: 

    def __init__(self, client_id='f761219356424233973b191ecfa812a5', client_secret='ec22780b46c340988ebef5afc3fb8a40'):
        # self.client_id = client_id
        # self.client_secret = client_secret
        self.sp = spotipy.Spotify(client_credentials_manager=
            SpotifyClientCredentials(client_id=client_id,client_secret=client_secret))
    
    def search_artist(self, artist_name, genre="metal"):
        search_str = f"{artist_name} genre={genre}"
        result = self.sp.search(search_str, type="artist", limit=15)

        for item in result["artists"]["items"]:
            if (item["name"].upper() == artist_name.upper()):
                return {"artist_id":item["id"],
                        "genres":item["genres"],
                        "followers":item["followers"],
                        "popularity":item["popularity"]}

    def search_albums(self, artist_id):
        print("TODO")