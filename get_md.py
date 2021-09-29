# MODULES
import os # path
import sys # argv, exit
import time # sleep
import json # dumps, load
import spotipy # Spotify API wrapper
from spotipy.oauth2 import SpotifyClientCredentials # Spotify API auth flow


# GLOBALS
PATH = os.path.abspath('.')
song_meta = {} # format: { 'song_id': {'feature_1':'val', 'feature_2':'val2', ...} }


# Create or retrieve metadata json
if not os.path.isfile(PATH + '\\metadata.json'):
    pass # if metadata doesn't already exist, let it remain an empty dict to be modified before output to json
else:
    with open(PATH + '\\metadata.json', 'rb') as mpath:
        song_meta = json.load(mpath)


# Generates conversion notes for Spotify API instrument key to user-readable values
keys = {}
if not os.path.isfile(PATH + '\\keys.json'):
    keys = {
            '0':'C',
            '1':'Db',
            '2':'D',
            '3':'Eb',
            '4':'E',
            '5':'F',
            '6':'Gb',
            '7':'G',
            '8':'Ab',
            '9':'A',
            '10':'Bb',
            '11':'B'
    }
    with open(PATH + '\\keys.json', 'w') as kpath:
        json.dump(keys, kpath)
else:
    with open(PATH + '\\keys.json', 'r') as kpath:
        keys = json.load(kpath)


# Activate Spotify API client
client_credentials_manager = SpotifyClientCredentials(sys.argv[1], sys.argv[2])
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


def main():

    results = sp.playlist(sys.argv[3])

    # Get track details
    for item in results['tracks']['items']:
        time.sleep(0.5) # prevent too many requests to API
        track_id = item['track']['id']
        if track_id in song_meta:
            continue # only add new entries in the playlist
        else:

            # Get metadata for track
            song_meta[track_id] = {}
            meta = sp.track(track_id)
            song_meta[track_id]['song'] = meta['name'] # song name
            song_meta[track_id]['album'] = meta['album']['name'] # album name song belongs to
            song_meta[track_id]['artist'] = ', '.join([artist['name'] for artist in meta['artists']]) # artist(s) name(s)
            song_meta[track_id]['popularity'] = meta['popularity'] # song popularity

            # Get audio features of the track
            features = sp.audio_features(track_id)[0]
            features['duration_ms'] = features['duration_ms']/60000 # ms to min
            for key, val in features.items():
                    
                # Convert Spotify API values to qualititative identifiers
                if key == 'key':
                    val = keys[str(val)]
                if key == 'mode':
                    if int(val) == 0:
                        val = 'Minor'
                    else:
                        val = 'Major'

                song_meta[track_id][key] = val

                # Breakout before reaching unwanted metadata
                if key == 'tempo':
                    break

    # Write metadata to JSON object
    with open(PATH + '\\metadata.json', 'wb') as mpath:
        mpath.write(json.dumps(song_meta, ensure_ascii=False).encode('utf-8')) # encoded for non-ASCII chars in track titles

    print(results['name']) # Send output back to main.py through STD_OUT

if __name__ == '__main__':
    main()

