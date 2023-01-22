# this script is responsible for fetching new popular indie songs and providing their names

from utils import getSpotifyApiKey
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "690df2c806074798a21b1c95eaa30c99"
spotifyApiKey = getSpotifyApiKey("")

PLAYLIST_ID = "7Lg2IGZJGAvGYqqUEuvqkU"  # my playlist id
sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=spotifyApiKey
    )
)

playlist = sp.playlist(PLAYLIST_ID)


class Track:
    name = ""
    artist = ""
    spotify_id = ""
    isAlreadyProcessed = False
    popularity_score = 0

    def __init__(self, name, artist, spotify_id, popularity_score) -> None:
        self.name = name
        self.artist = artist
        self.spotify_id = spotify_id
        self.popularity_score = popularity_score

    def getName(self) -> str:
        return self.name

    def getArtist(self) -> str:
        return self.artist

    def getSpotifyID(self) -> str:
        return self.spotify_id

    def getPopularityScore(self) -> int:
        return self.popularity_score

    def isAlreadyProcessed() -> bool:
        isAlreadyProcessed = True
        return isAlreadyProcessed


SONGS = []
while True:
    while True:
        items = playlist.get("tracks").get("items")
        size = int(playlist["tracks"]["total"])
        print(size)
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
    