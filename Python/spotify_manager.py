# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
from rapidfuzz import fuzz, process
# from fuzzywuzzy import fuzz, process
import spotipy, sys, pprint, json, Levenshtein

class SpotifyManager: 

    def __init__(self, client_id='f761219356424233973b191ecfa812a5', client_secret='ec22780b46c340988ebef5afc3fb8a40'):
        self.sp = spotipy.Spotify(client_credentials_manager=
            SpotifyClientCredentials(client_id=client_id,client_secret=client_secret))
    
    def search_artist(self, artist_name, genre="metal"):
        search_str = f"{artist_name} genre:{genre}"
        result = self.sp.search(search_str, type="artist", limit=15)
        pprint.pprint(result)
        # TODO Sonuc bulamazsa case
        for item in result["artists"]["items"]:
            if (item["name"].upper() == artist_name.upper()):
                return {"artist_id":item["id"],
                        "genres":item["genres"],
                        "followers":item["followers"],
                        "popularity":item["popularity"]}

    def search_albums(self, artist_id):
        # Get albums of the artist
        result = self.sp.artist_albums(artist_id, album_type="album", limit=50)
        pprint.pprint(result)


        # Group every album according to their name similarity

        # Count each group and add number as an information

        # If an album is part of groups above, return how many iterations
        # If not, return 0 or 1
        for item in result["items"]:
            albums.append({"id":item["id"],
                        "name":item["name"],
                        "release_date":item["release_date"],
                        "precision":item["release_date_precision"],
                        "track_count":item["total_tracks"]})
        return albums
    
    def match_albums(albums)

        # Match Live/Remaster/Deluxe Edition albums
        albums = []
        groups = []
        album_names = []
        for album in albums:
            album_names.append(album["name"])

        for album in albums:
            in_group = False
            # Did we match this album before?
            for group in groups:
                if album["name"] in group:
                    in_group = True
                    continue
            if not in_group:
                temp_list = []
                # FuzzMatch with every other album
                fuzzed_albums = process.execute(album["name"], album_names,
                    scorer=fuzz.partial_token_set_ratio, limit=None)
                # Compare fuzz results
                for fuzz in fuzzed_albums:
                    # Number can be changed
                    if (fuzz[1] > 90):
                        temp_list.append(fuzz[0])                
                groups.append(temp_list)
