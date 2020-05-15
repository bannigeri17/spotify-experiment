import spotify_query as spq
import copy
import numpy as np

requester = spq.requester()

ranged_feature_dict = {
    'danceability': (0.65, 0.70),
    'energy': (0.56, 0.66),
    'key': (1, 1),
    'loudness': (-10, -4),
    'mode': (0, 1),
    'speechiness': (0, 0.6),
    'acousticness': (0, 0.7),
    'instrumentalness': (0, 0.1),
    'liveness': (0, 0.41),
    'valence': (0.2, 0.6),
    'tempo': (110, 160)
}

id_2012 = '1t4NkaqXYRl8g5FTNBUVgG'                  # spotify playlist id for 2012 (the vibe playlist hahah)
quasi_id = '17bwhvUEbRFXvcCVbd4nXK'                 # spotify playlist id for quasi (the big data dump playlist)

feature_data_2012, trax_2012 = requester.get_playlist_features_data(id_2012)    # feature data and ids for tracks already in 2012

for key in feature_data_2012:
    if key is not 'mode':
        key_mean = np.mean(feature_data_2012[key])
        key_stdev = np.std(feature_data_2012[key])
        ranged_feature_dict[key] = (key_mean - key_stdev, key_mean + key_stdev)

print(ranged_feature_dict)

lis_2012 = requester.spotify.playlist(id_2012)
n_2012 = lis_2012['tracks']['total']
temp = 0
temp_offs = 0
while(temp < n_2012):
    temp_query = requester.spotify.playlist_tracks(quasi_id,offset=temp_offs)
    temp_list = temp_query['items']
    for t in temp_list:
        temp += 1
        if t is not None and not t['is_local']:
            temp_track = t['track']
            trax_2012.append(temp_track['id'])
    temp_offs += 100

print(trax_2012)
print(len(trax_2012))

list = requester.spotify.playlist(quasi_id)
num_tracks = list['tracks']['total']
#print(num_tracks)
total = 0
cur_offset = 0
num_accepted = 0
num_rejected = 0

subset_list = []

while(total < num_tracks):
    tracks_query = requester.spotify.playlist_tracks(quasi_id, offset = cur_offset)
    track_list = tracks_query['items']
    for item in track_list:
        total += 1
        #print(item)
        if item is not None and not item['is_local']:
            track = item['track']
            #if track is not None and 'id' in track:
            cur_id = track['id']
            #print("trying "+track['name']+" by "+track['artists'][0]['name'])
            if cur_id not in trax_2012:
                try:
                    cur_feats = requester.get_song_features(cur_id)
                    in_range_count = 0
                    for feat in ranged_feature_dict:
                        feat_min,feat_max = ranged_feature_dict[feat]
                        #print(str(feat_min)+", "+ str(feat_max) + " : " + str(cur_feats[feat]))
                        if feat_min <= cur_feats[feat] <= feat_max:
                            in_range_count += 1
                            #print("fits for "+feat)
                        #else:
                            #print("breaks for "+ feat)
                    if in_range_count >= 10:
                        print("added " + track['name']+" by "+track['artists'][0]['name'])
                        subset_list.append((track['name'], track['artists'][0]['name']))
                        num_accepted += 1
                    else:
                        num_rejected += 1
                except TypeError:
                    print("Features not found, but moving on")
            else:
                num_rejected += 1
                #print(track['name']+" already in 2012")
    #print(cur_offset)
    #print(features_dict)
    cur_offset += 100
    print(str(cur_offset) + " tracks processed...")
    print(str(num_accepted) + " tracks accepted...")
    print(str(num_rejected) + " tracks rejected...")

accepted_rate = float(num_accepted)/total
accepted_perc = accepted_rate*100
print(str(accepted_perc)+ "% of quasi could fit in 2012")
for t, a in subset_list:
    print(t+" by "+a)