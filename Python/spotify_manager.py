# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
from rapidfuzz import process
from rapidfuzz.fuzz import partial_token_set_ratio
from spotipy.exceptions import SpotifyException
# from fuzzywuzzy import fuzz, process
import spotipy, sys, pprint, json, glob, datetime as dt, time, pandas as pd, re;

class SpotifyManager: 

    greenlist = set(["metal","rock","nwobhm","punk","core","nwothm","ponk","h8000","straight edge","ukhc","uk82","beatdown","nyhc","grunge","djent","death",
                "death","skramz","melodeath","grind","thrash","hardcore","post-hardcore","screamo","screamocore","deathrash","sasscore","swancore",
                "pornogrind","orgcore","mathcore","oi","slayer","emocore","thall","dreamo","doom","deathcore","shred","visual","shoegaze","goregrind",
                "noisecore","heavy psych","black","beatdown","metalcore","sludgecore","powerviolence","latincore","nintendocore","ramonescore",
                "trancecore","gymcore","easycore","queercore","swancore","electronicore","jazzcore","doomcore","crust","italogaze",])

    def __init__(self, client_id='f761219356424233973b191ecfa812a5', client_secret='ec22780b46c340988ebef5afc3fb8a40'):
        self.sp = spotipy.Spotify(client_credentials_manager=
            SpotifyClientCredentials(client_id=client_id,client_secret=client_secret))
    
    def search_all_artists(self, stop=0):
        
        FILE_COUNTER_STRING = 'bands_counter.txt'
        RESULT_FILE_STRING = 'all_artists.csv'

        start_index = 0
        if glob.glob(FILE_COUNTER_STRING):
            with open(FILE_COUNTER_STRING,'r') as file:
                file_index = file.read().strip()
                if file_index:
                    start_index = int(file_index)
                print(f"REMOVE THIS!!! all_band_names start index: {start_index}")
        # Not calling this since we're doing same work on Scala Spark
        # self.gather_band_names()

        if not glob.glob(RESULT_FILE_STRING):
            with open (RESULT_FILE_STRING, 'w') as target:
                target.write(',artist_name,artist_id,genres,followers,popularity\n')

        artists = {}
        no_results = 0
        non_matched = 0
        multiple_matched = 0
        regular_matched = 0
        # counter = 0

        with open ("all_band_names.txt", "r+") as source:
            for i,line in enumerate(source.readlines()[start_index:],start_index):
                name = line.strip()
                matched = self.search_artist(name,limit=10)
                cnt_mtch = len(matched[0])
                if cnt_mtch == 1:
                    artists.update(matched[0])
                    regular_matched += 1
                elif cnt_mtch == 0:
                    if (matched[1]):
                        non_matched += 1
                    else:
                        no_results += 1
                elif cnt_mtch > 1:
                    print(f'Multiple match on: {matched[0]}')
                    multiple_matched += (cnt_mtch - 1)
                    artists.update(matched[0])
                else:
                    pass

                # counter += 1
                if (i + 1) % 1250 == 0:
                    print(f'Length of artist dataframe is: {len(artists)}')
                    print(f'tell() returns: {source.tell()}')
                    df = pd.DataFrame.from_dict(artists, orient='index')
                    df.to_csv(RESULT_FILE_STRING,mode='a',index=True,header=False)
                    with open(FILE_COUNTER_STRING,'w') as file:
                        file.write(str(i+1))
                    artists = {}
                    if (i+1)>=stop:
                        break
                    print(f"\n{dt.datetime.now()}  ---  XXXXX Current line is {i + 1} XXXXX\n")
            
        print("\n FINAL RESULTS \n")
        # print(f"Dictionary contains {len(artists)} many artists.") # \nFirst element is:")
        # pprint.pprint(artists[0])
        print("Last element is:")
        # pprint.pprint(artists[-1])
        print(f"Normal matches: {regular_matched}")
        print(f"Artists deleted from genre matching: {non_matched},") 
        print(f"Spotify couldn't match our band name: {no_results},") 
        print(f"Multiple matches are {multiple_matched}")

        time = dt.datetime.now()
        if artists:
            print(f"Writing {len(artists)} artists that is left.")
            df = pd.DataFrame.from_dict(artists, orient='index')
            df.to_csv(RESULT_FILE_STRING,mode='a',index=True,header=False)
            print("Remaining write operation should be succesfull")
        # df.to_csv(f"First_6000_Artists_{time.month}_{time.day}_{time.hour}_{time.minute}.csv")
    
    def search_all_albums(self, stop=0):
        # TODO 

    def fix_spark_csv_headers(self):
        # If spark left csv files without headers, this fixes it
        for mad_file in glob.glob('../Scala/mad_plus/*.csv'):
            with open(mad_file, 'r') as original: data = original.read()
            with open(mad_file, 'w') as modified: modified.write("mad_band_name,mad_genres\n" + data)

    def format_spark_madplus(self):
        # Assumes fix_spark_csv_headers has been invoked
        # Gets Spark created all_mad_artists.csv file and merges it with 
        # python created all_artists.csv. Writes it to a file.
        # PS: Don't forget to change python output csv's header manually or smt.
        # Required format: 
        # sp_artist_id,mad_artist_name,sp_artist_name,sp_artist_id,sp_genres,sp_followers,sp_popularity
        files = glob.glob('../Scala/mad_plus/*.csv')
        df_mp = pd.concat([pd.read_csv(files[2]),pd.read_csv(files[0]),pd.read_csv(files[1])],
            ignore_index=True)
         df_all = pd.merge(df_mp,df_py,how='left',left_on='mad_band_name',right_on='mad_artist_name')
         df_all = df_all.drop(axis='columns',labels=['mad_artist_name','sp_artist_id.1'])
         df_all.to_csv('merged_mp_py_artists.csv')

    def gather_band_names(self):
        path = '/home/kaan/Repos/metal_dataset/'
        FILE_NAME = 'all_band_names.txt'
        all_bands = []

        if glob.glob(FILE_NAME):
            print('gather_band_names() found a file already created')
            return FILE_NAME

        # Gather all file names from all genres
        list_of_files = glob.glob(path + '*_bands.txt')
        for name in list_of_files:
            all_bands.append(name)

        # Assumes the intended file exists and returns the name directly.
        with open(FILE_NAME, "w") as target_file:
            # Read all files and write lines to a set
            lines = set()
            for genre_file in all_bands:
                with open(genre_file, "r") as source_file:
                    temp_set = set(source_file.readlines())
                    lines.update(temp_set)
            # Write set's lines to target file
            for line in lines:
                target_file.write(line)
        return FILE_NAME

    def get_trve_artists(self):
        # read artist name file
        
            # iterate with search_artist
            
            # write results to another file 
        return True

    def search_artist(self, artist_name, genre="metal", limit=50):
        # Genre'yi query'e eklemek istersen lazim olacak alttaki
        # search_str = f"{artist_name}"
        result = {}
        # TODO: try catch'ten cikar? Performans etkilerse cikar
        # cunku spotiPy kendisi try catch mekanizmali calisiyor olabilir.
        # Slight difference var diyorlar cok major degilmis fark.
        try:
            result = self.sp.search(artist_name, type="artist", limit=limit)
        except SpotifyException as se:
            # TODO Else ekle
            if se.http_status == 429:
                print(f"{dt.datetime.now()} 429 429 429 429 429 429 429 429 429 429")
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
                    print(e.args)
        except Exception as e:
            print(f"{dt.datetime.now()} - {e.args}")
        # pprint.pprint(result)
        matched = {}
        if result:
            if len(result["artists"]["items"]):
            # item = result["artists"]["items"][0]
                for item in result["artists"]["items"]:
                    if (item["name"].upper() == artist_name.upper()):
                        # For real trve experience, only take ones within greenlist
                        for genre in item['genres']:
                            words = re.split('\\-|\\ ', genre)
                            if self.greenlist.intersection(words):
                                matched.append({"mad_artist_name"   :artist_name,
                                            "spotify_artist_name"   :item["name"],
                                            "spotify_artist_id"     :item["id"],
                                            "spotify_genres"        :item["genres"],
                                            "followers"             :item["followers"],
                                            "popularity"            :item["popularity"]})
                                # 22.12.22 basliklari guncelledim ama sonuc dosyada hala hatali btw.
                                # matched[item["id"]] = {"test_name":artist_name,
                                #                         "artist_name":item["name"],
                                #                         "artist_id"  :item["id"],
                                #                         "genres"     :item["genres"],
                                #                         "followers"  :item["followers"],
                                #                         "popularity" :item["popularity"]}
            else:
                # Spotipy covldn't find any resvlts
                return (matched,False)
        # print(f"Spotipy matched {len(matched)} many artists for {artist_name}")
        # Had some resvlts and went throvgh a genre search
        return (matched,True)

    def search_albums(self, artist_id):
        # Get albums of the artist
        result = self.sp.artist_albums(artist_id, country="US", album_type="album,single", limit=50)
        # pprint.pprint(result)
        albums = []
        if result['items']:
            for item in result['items']:
                temp = {'album_group'       :item['album_group'],
                        'spotify_album_id'  :item['id'],
                        'album_name'        :item['name'],
                        'album_release_date':item['release_date']}
                       #'album_total_tracks':item['total_tracks']
                albums.append(temp)
        
        return albums


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

