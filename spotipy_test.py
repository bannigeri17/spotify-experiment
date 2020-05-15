import re

import spotipy as sp
import spotify_query
from client_info import client_id, client_secret

scope = 'user-library-read'

cl = sp.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

auth_token = cl.get_access_token()

spotify = sp.Spotify(auth=auth_token)

query = spotify.search(q="track:alright artist:kendrick lamar", type='track', limit=10)

obj = query['tracks']  # this is the body of the query results

items = obj['items']  # this is a list of dictionaries that store the information of each returned item from the query

'''
TRACK QUERIES:
Each item dictionary contains the following keys:
    1. album: a dictionary representing an album object corresponding to the album the track is on
    2. artists: a list of dictionaries representing artist objects for the artists who performed the track
    3. available markets: a list of 'markets' where the track is available for listening, represented by country code
    4. disc number: in case the album is split into multiple discs, which disc is the track we want on?
    5. duration_ms: length of the song in milliseconds
    6. explicit: does the song have any no-no words?
    7. external_ids: any known external ids through other platforms/indexes
    8. external_urls: any known external urls through other platforms/indexes
    9. href: Web API endpoint
    10. id: ID through Spotify platform, we want to use this for the feature extraction
    11. is_local: is the track from a local file
    13. name: name of the track
    14. popularity: on a scale of 1 to 100, how popular is the song
    15. preview_url: a link to some 30 second preview; this can be null
    16. track_number: on the album, where is this track sequenced?
    17. type: object type, should be 'track'
    18. uri: Spotify URI for the track
'''

for item in items:
    print(item)

obj_wanted = items[0]

obj_id = obj_wanted['id']

feat = spotify.audio_features(obj_id)



print(feat)

print("what's your favorite album?")
u_out = input()

re_song_match = re.compile(r'(.*)(?:\sby\s)(.*)')  # simple reg ex matching a track and artist,
# a reasonable format to be presented with in terms of a user's favorite track

m = re_song_match.match(u_out)

spq = spotify_query.requester()

if m:
    song_str = m.group(1)
    artist_str = m.group(2)
    print(artist_str)
    query_str = "album:"+song_str+" artist:"+artist_str
    print(query_str)
    user_q = spotify.search(query_str,type="album",limit=10)
    user_object = user_q['albums']
    user_results = user_object['items']
    for result in user_results:
        print(result)
    user_album = user_results[0]
    user_album_id = user_album['id']
    tracks = spotify.album_tracks(user_album_id)

    feat_dict = spq.get_album_avg_features(user_album_id)
    for f in feat_dict:
        print(f)
        print(feat_dict[f])
        print("--------")


print("who's your favorite artist:")
u_q = input()

print(spq.get_artist_genres(u_q))
ar = spq.search_for_artist(u_q)
user_artist = ar[0]
print(ar)
artist_id = user_artist['id']
feat_dict = spq.get_artist_avg_features(artist_id)
for f in feat_dict:
    print(f)
    print(feat_dict[f])
    print("-------------------------")

print(spq.search_for_song("i dont know","drake"))