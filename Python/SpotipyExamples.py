# shows artist info for a URN or URL

from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
import spotipy, sys, pprint, json

if len(sys.argv) > 1:
    artistName = sys.argv[1]
else:
    artistName = 'Iron maiden'

search_str = artistName + ' genre=metal'

sp = spotipy.Spotify(client_credentials_manager=
    SpotifyClientCredentials(client_id='f761219356424233973b191ecfa812a5',client_secret='ec22780b46c340988ebef5afc3fb8a40'))
text_encoded = quote(search_str)
# print(text_encoded)
result = sp.search(search_str, type="artist", limit=20)
pprint.pprint("total result is: %s" % result["artists"]["total"])


for item in result["artists"]["items"]:
    if (item["name"] == artistName):
        print("We've made it! " + item["name"])


# parsed = json.loads(result)
# print(parsed("name"))

# f = open("demoResults.txt","w")
# f.write(search_str + "\n" )
# f.write(result.__str__)
# f.close()
