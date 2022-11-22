# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
from rapidfuzz import process
from rapidfuzz.fuzz import partial_token_set_ratio
# from fuzzywuzzy import fuzz, process
import spotipy, sys, pprint, json, glob, datetime as dt, time, pandas as pd;

class SpotifyManager: 

    def __init__(self, client_id='f761219356424233973b191ecfa812a5', client_secret='ec22780b46c340988ebef5afc3fb8a40'):
        self.sp = spotipy.Spotify(client_credentials_manager=
            SpotifyClientCredentials(client_id=client_id,client_secret=client_secret))
    
    def test_all_artists(self):
        self.gather_band_names()
        artists = []
        non_matched = 0
        multiple_matched = 0
        counter = 1
        with open ("all_band_names.txt", "r") as source:
            for line in source.readlines():
                name = line.strip()
                if counter % 250 == 0:
                    if counter > 6000:
                        break
                    print(f"\n{dt.datetime.now()}  ---  XXXXX Counter is {counter} XXXXX\n")
                    # if len(artists) > 5:
                    #     break
                matched = self.search_artist(name,limit=10)
                cnt_mtch = len(matched)
                if cnt_mtch == 1:
                    artists.append(matched[0])
                elif cnt_mtch == 0:
                    non_matched += 1
                elif cnt_mtch > 1:
                    multiple_matched += (cnt_mtch - 1)
                    # print(f"Matched multiple on {name}")
                    artists.extend(matched)
                else:
                    pass
                counter += 1
            
            print("\n FINAL RESULTS \n")
            print(f"Dictionary contains {len(artists)} many artists.\nFirst element is:")
            pprint.pprint(artists[0])
            print("Last element is:")
            pprint.pprint(artists[-1])
            print(f"Non matched count is {non_matched},") 
            print(f"and multiple matches are {multiple_matched}")
        
    def gather_band_names(self):
        path = '/home/kaan/Repos/metal_dataset/'
        all_bands = []

        # Gather all file names from all genres
        for name in glob.glob(path + '*_bands.txt'):
            all_bands.append(name)

        with open("all_band_names.txt", "w+") as target_file:
            # Read all files and write lines to a set
            lines = set()
            for genre_file in all_bands:
                with open(genre_file, "r") as source_file:
                    temp_set = set(source_file.readlines())
                    lines.update(temp_set)

            # Write set's lines to target file
            target_file.seek(0,0)
            for line in lines:
                target_file.write(line)
        
    def get_trve_artists(self):
        # read artist name file
        
            # iterate with search_artist
            
            # write results to another file 
        return True

    def search_artist(self, artist_name, genre="metal", limit=50):
        # Genre'yi query'e eklemek istersen lazim olacak alttaki
        # search_str = f"{artist_name}"
        result = []
        try:
            result = self.sp.search(artist_name, type="artist", limit=limit)
        except SpotifyException as se:
            if se.http_status == 429:
                print("429 429 429 429 429 429 429 429 429 429")
                try:
                    retry_time = int(se.headers['retry-after'])
                    print(f"Will sleep for {retry_time} seconds")
                    time.sleep(retry_time + 1)
                    result = self.sp.search(artist_name, type="artist", limit=limit)
                except ValueError:
                    print("Json parse edemedim :'(")
                except SpotifyException as se2:
                    print("Yet another Spotify Exception with parameters:")
                    print(f"Http Status: {se2.http_status}\nCode: {se2.code}\nMsg: {se2.msg}\nReason: {se2.reason}\nHeaders:")
                    pprint.pprint(se2.headers)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e.args)
        # pprint.pprint(result)
        # TODO Sonuc bulamazsa case
        matched = []
        for item in result["artists"]["items"]:
            if (item["name"].upper() == artist_name.upper()):
                matched.append({"artist_name":item["name"],
                            "artist_id":item["id"],
                            "genres":item["genres"],
                            "followers":item["followers"],
                            "popularity":item["popularity"]})
        # print(f"Spotipy matched {len(matched)} many artists for {artist_name}")
        return matched

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

