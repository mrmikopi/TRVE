# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
from rapidfuzz import process
from rapidfuzz.fuzz import partial_token_set_ratio
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
        result = self.sp.artist_albums(artist_id, country="US", album_type="album", limit=50)
        # pprint.pprint(result)
        albums = []

        # Group every album according to their name similarity

        # Count each group and add number as an information

        # If an album is part of groups above, return how many iterations
        # If not, return 0 or 1
        for item in result["items"]:
            albums.append({"id":item["id"],
                        "name":item["name"],
                        "release_date":item["release_date"],
                        "track_count":item["total_tracks"]})
        # Match Live/Remaster/Deluxe Edition albums
        # albums = match_albums(albums)

        return albums
    
    # TODO Not finished. Might be used for eliminating "Deluxe edition" albums.
    def match_albums(self, albums):

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
                    break
            if not in_group:
                temp_list = []
                # FuzzMatch with every other album
                fuzzed_albums = process.extract(query=album["name"], choices=album_names,
                    scorer=partial_token_set_ratio, limit=None)
                matched_album_count = 0
                # Compare fuzz results
                for fuzz in fuzzed_albums:
                    # fuzz ratio can be changed
                    if (fuzz[1] > 90):
                        temp_list.append(fuzz[0])                
                        matched_album_count += 1
                groups.append(temp_list)
                album["related_albums"] = {"related_album_names":temp_list,"count":len(temp_list)}
            else:
                # Add key: Related Albums
                album["related_albums"] = {"related_album_names":temp_list}


        return albums

