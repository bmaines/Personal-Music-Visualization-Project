#Install spotipy and pandas before running

import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='< INSERT-CLIENT-ID >', client_secret='< INSERT-CLIENT-SECRET >', redirect_uri='< INSERT-REDIRECT-URI >', scope="playlist-read-private"))

# prompt the user to enter the playlist ID
##playlist_id = input("Enter the playlist ID: ")
playlists = sp.current_user_playlists()['items']
print("Select a playlist:")
for i, playlist in enumerate(playlists):
    print(f"{i+1}. {playlist['name']}")

choice = int(input()) - 1
playlist_id = playlists[choice]['id']

# initialize an empty list to store the track data
tracks = []

# set the initial offset value to 0
offset = 0

# retrieve the first 50 tracks from the playlist
results = sp.playlist_items(playlist_id, limit=50, offset=offset)

# initialize an empty set to store the track IDs
track_ids = set()

# iterate through the paginated results and append the track data to the list
while results['items']:
    for item in results['items']:
        track = item['track']
        if track is not None and track['id'] not in track_ids: features = sp.audio_features(track['id'])
        album = track['album'] #test line
        track_data = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'duration_ms': track['duration_ms'],
            'popularity': track['popularity'],
            'id': track['id'],
            'uri': track['uri'],
            'track_num': track['track_number'],
            'explicit': track['explicit'],
            'bpm': features[0]['tempo'] if features and features[0] and 'tempo' in features[0] else None,
            'key': features[0]['key'] if features and features[0] and 'key' in features[0] else None,
            'mode': features[0]['mode'] if features and features[0] and 'mode' in features[0] else None,
            'danceability': features[0]['danceability'] if features and features[0] and 'danceability' in features[0] else None,
            'energy': features[0]['energy'] if features and features[0] and 'energy' in features[0] else None,
            'loudness': features[0]['loudness'] if features and features[0] and 'loudness' in features[0] else None,
            'speechiness': features[0]['speechiness'] if features and features[0] and 'speechiness' in features[0] else None,
            'acousticness': features[0]['acousticness'] if features and features[0] and 'acousticness' in features[0] else None,
            'instrumentalness': features[0]['instrumentalness'] if features and features[0] and 'instrumentalness' in features[0] else None,
            'audience_presence': features[0]['liveness'] if features and features[0] and 'liveness' in features[0] else None,
            'positivity': features[0]['valence'] if features and features[0] and 'valence' in features[0] else None,
            'time_signature': features[0]['time_signature'] if features and features[0] and 'time_signature' in features[0] else None
        }
        tracks.append(track_data)
        track_ids.add(track['id'])
    
    # increment the offset by 50 to retrieve the next page of results
    offset += 50
    results = sp.playlist_items(playlist_id, limit=50, offset=offset)

# create a Pandas DataFrame from the track data
df = pd.DataFrame(tracks)

# export the DataFrame to an Excel sheet
df.to_excel("songs.xlsx", index=False)


