import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
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

#data:
pas_path = 'Steamlit_Spotify/Data/Artist.csv'
PAS_info_full = pd.read_csv(pas_path)

#get all unmastered artist to first master
PAS_info_new = PAS_info_full[PAS_info_full['Mastered Name'].isna()]


if not PAS_info_new.empty: #If unmaster artist found
    #getting unique new artist to reduce api calls to Spotify
    PAS_info_new = PAS_info_new.groupby(['Insured']).sum().reset_index()[['Insured']]


    #mastering and enhancing the new artist that are added to the database
    master_artist = []
    for name in PAS_info_new['Insured']:
        results = sp.search(q= name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            dict = {'Insured': name,
                    'Mastered Name': artist['name'],
                    'Genre': artist['genres'],
                    'Spotify URI': artist['uri'],
                    'Image URL': artist['images'][1]['url'],
                    'Image Width': artist['images'][1]['width'],
                    'Image Height': artist['images'][1]['height']}
            master_artist.append(dict)
    master_artist = pd.DataFrame(master_artist)

    #merging with PAS info to fill in the unmastered and enhancing information
    PAS_info_mastered = PAS_info_full.merge(master_artist, on = 'Insured', how = 'left', suffixes=('_old', '_new'))

    columns = ['Mastered Name', 'Genre', 'Image URL', 'Image Width', 'Image Height', 'Spotify URI']
    for col in columns:
        #chossing the new value if the orginial column value is nul, else sticking with the orginial value
        PAS_info_mastered[f'{col}'] = PAS_info_mastered[f'{col}_old'].where(PAS_info_mastered[f'{col}_old'].notnull(), PAS_info_mastered[f'{col}_new'])
        PAS_info_mastered = PAS_info_mastered.drop([f'{col}_old',f'{col}_new'],axis=1)


    #Write mastered info back into DB
    PAS_info_mastered.to_csv(pas_path, index=False)


#Loading in mastered PAS information (again)
PAS_info_mastered = pd.read_csv(pas_path)

#Adding music of new artist to playlist

#Get tracks from the playlist
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
tracks = sp.tracks(track_uris)

#Finding current artist in the playlist
current_artist_playlist = [track['artists'][0]['name'] for track in tracks['tracks']]

#Checking which are not in the playlist ---> need to do fuzzy match instead of exact match
artist_to_add = PAS_info_mastered[~PAS_info_mastered['Mastered Name'].isin(current_artist_playlist)]
artist_to_add_unique = artist_to_add.groupby('Mastered Name').first().reset_index()

#Find track ids
tracks_to_add = []
for i in range(len(artist_to_add_unique)):
    artist = artist_to_add_unique.iloc[i]
    response = sp.artist_top_tracks(artist['Spotify URI'])
    for track in response['tracks'][:1]:
        tracks_to_add.append(track['uri'])
        print(artist['Mastered Name'],track['name'], track['uri'])

#Add tracks to playlist
sp.playlist_add_items(playlist_URI, tracks_to_add) 


#constrcting the webapp