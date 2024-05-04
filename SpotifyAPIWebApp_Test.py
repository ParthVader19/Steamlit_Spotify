import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pprint
'''
To do:
1. Generate database of artist and gross premium: -done
    -Insured, class of business, gross guarantees
2. Look at the InsurX playlist and find artist -done
3. Find artist from database that are not in the playlist -done
4. Search artist on Spotify -done
5. Find top songs -done
6. Add top 5 songs to Spotify Playlist if new songs sound -done
    -Run the method at a specific time of the day 
7. Steamlit App
'''

#data:

PAS_info = {
    1 : {
        'insured': 'Taylor Swift',
        'Premium': 100e6,
        'dateBound': '10/12/2023'
    },
    2 : {
        'insured': 'Fred Again',
        'Premium': 3e6,
        'dateBound': '14/02/2024'
    },
    3 : {
        'insured': 'Green Day',
        'Premium': 12e6,
        'dateBound': '11/11/2023'
    },
    4 : {
        'insured': 'Dried Spider',
        'Premium': 100e6,
        'dateBound': '23/04/2024'
    },
    5 : {
        'insured': 'Kali Uchis',
        'Premium': 13e6,
        'dateBound': '15/03/2024'
    },
    5 : {
        'insured': 'Steve Lacy',
        'Premium': 9e5,
        'dateBound': '09/02/2024'
    },
}

PAS_info = pd.DataFrame(PAS_info).T


#get from https://developer.spotify.com. Setting up credintals
cid = '1ade2ed8312744d18c4cb6320fcdb33a'
secret = 'bf807d1d0496411f9ebd6b8c4a033230'
scope = "playlist-modify-private"

#Authentication - without user
# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=cid,
                                client_secret=secret,
                                redirect_uri='http://localhost:8888/callback',
                                scope=scope
                                ))


#InsurX vibes playlist
playlist_link = "https://open.spotify.com/playlist/4Z5uQy7BPvZDZD67mFEdy8"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

#Get tracks from the playlist
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
tracks = sp.tracks(track_uris)

#Finding current artist in the playlist
current_artist_playlist = [track['artists'][0]['name'] for track in tracks['tracks']]

#Checking which are not in the playlist ---> need to do fuzzy match instead of exact match
artist_to_add = PAS_info[~PAS_info['insured'].isin(current_artist_playlist)]

new_artist = []

#Search for artist
for name in artist_to_add['insured']:
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        dict = {'name': artist['name'],
                'genre': artist['genres'],
                'uri': artist['uri'],
                'image url': artist['images'][0]['url'],
                'image width': artist['images'][0]['width'],
                'image height': artist['images'][0]['height']}
        new_artist.append(dict)

#Find track ids
tracks_to_add = []
for artist in new_artist:
    response = sp.artist_top_tracks(artist['uri'])
    for track in response['tracks'][:1]:
        tracks_to_add.append(track['uri'])
        print(artist['name'],track['name'], track['uri'])

#Add tracks to playlist
sp.playlist_add_items(playlist_URI, tracks_to_add) 



