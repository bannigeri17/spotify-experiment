import spotify_query as spq
import numpy as np
import matplotlib.pyplot as plt

def generateHistDistGraph(features_data, key, bins = 25):
    plt.hist(features_data[key], bins=bins)
    plt.title('Distribution of '+key+' feature for given playlist')
    plt.show()

playlistID = '1t4NkaqXYRl8g5FTNBUVgG'

requester = spq.requester()

playlist_features_data = requester.get_playlist_features_data(playlistID)

for key in playlist_features_data:
    print(key+": ")
    print("\taverage:\t"+str(np.mean(playlist_features_data[key])))
    print("\tstandard dev:\t"+str(np.std(playlist_features_data[key])))
    print("\tmedian:\t"+str(np.median(playlist_features_data[key])))


plt.style.use('ggplot')

for key in playlist_features_data:
    generateHistDistGraph(playlist_features_data, key)
