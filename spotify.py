# this script is responsible for fetching new popular indie songs and providing their names

from utils import getSpotifyApiKey
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Track import Track
CLIENT_ID = "690df2c806074798a21b1c95eaa30c99"
spotifyApiKey = getSpotifyApiKey("")

PLAYLIST_ID = "7Lg2IGZJGAvGYqqUEuvqkU"  # my playlist id
sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=spotifyApiKey
    )
)

playlist = sp.playlist(PLAYLIST_ID)


SONGS = []
while True:
    while True:
        items = playlist.get("tracks").get("items")
        size = int(playlist["tracks"]["total"])
        for i in range(size):
            track = items[0].get("track")
            artistName = track.get("artists")[0].get("name")
            track = Track(
                name=track["name"],
                artist=artistName,
                spotify_id= track["id"],
                popularity_score= track["popularity"],
            )
            SONGS.append(track)
        
        if playlist.get("tracks").get("next") == None:
            break
        playlist["tracks"] = playlist.get("tracks").get("next")
    if playlist.get("next")== None:
        break
    playlist = playlist.get("next")