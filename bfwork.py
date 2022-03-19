import requests
from collections import deque
from spotifyids import *

# spotifyids.py contains headers (client_id, client_secret, token), and playlist_url variables

# POSSIBLE YT ENDPOINT: https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&q=YOURKEYWORD&type=video&key=YOURAPIKEY
# Retrieve etag, append to url to create yt-dl info
# Consolidate excess requests into single variable

class BotFly:
    def retrieve_playlist_info():
        # Define total as the total number of songs in the playlist
        total = dict(requests.get(url=playlist_url, headers=headers, params=(f"fields=total")).json())['total']
        print(f'Playlist ID = {playlist_id}')
        print(f'Retrieving playlist info from Spotify...')

        # Send initial GET request 
        titles_raw = dict(requests.get(url=playlist_url, headers=headers, params=(f"fields=items(track(name))")).json())
        artists_raw = dict(requests.get(url=playlist_url, headers=headers, params=(f"fields=items(track(artists(name)))")).json())
        print('Creating YouTube search info...')

        # Define incrementing and index variables; set artist_lst_raw to the unrefined list of artists
        song_index = 0
        artist_index = 0
        offset = 0
        artist_lst_raw = artists_raw["items"][song_index]["track"]["artists"]
        temp_dq = deque()
        query_dq = deque()
        
        # Spotify API only returns up to 100 items by default. Using offset, we can make new requests as needed to get every song from the playlist
        # offset will define where to begin the next request and also count every song
        # offset - 1 will account for the last song in the playlist
        while offset - 1 < total:
            if offset % 100 == 0 and offset != 0:
                titles_raw = dict(requests.get(url=playlist_url, headers=headers, params=(f"fields=items(track(name))&offset={offset}")).json())
                artists_raw = dict(requests.get(url=playlist_url, headers=headers, params=(f"fields=items(track(artists(name)))&offset={offset}")).json())
                offset += 1
                song_index = 0
            else:
                # Add every artist for a given song to temp_dq to later pair
                while artist_index < len(artist_lst_raw):
                    artist_lst_raw = artists_raw["items"][song_index]["track"]["artists"]
                    artist = artist_lst_raw[artist_index]["name"]
                    temp_dq.append(artist)
                    artist_index += 1
                else:
                    # Once artists have been selected, match them with song to form a single list element
                    song = titles_raw["items"][song_index]["track"]["name"]
                    temp_dq_str = ' '.join(temp_dq)
                    
                    # Adding 'lyrics' selects videos that just have the music in most cases
                    # May need to check genre to properly search instrumental music like classical and jazz
                    query_dq.append(song + ' ' + temp_dq_str + ' lyrics')

                    # Reset and increment variables to set up for next song
                    artist_index = 0
                    song_index += 1
                    offset += 1
                    temp_dq = deque()
        print(query_dq)

BotFly.retrieve_playlist_info()