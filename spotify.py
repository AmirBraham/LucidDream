# this script is responsible for fetching new popular indie songs and providing their names

from utils import getSpotifyApiKey
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Track import Track
from db import addTrack
from typing import List


def fetchPlaylistSongs(PLAYLIST_ID):
    CLIENT_ID = "690df2c806074798a21b1c95eaa30c99"
    spotifyApiKey = getSpotifyApiKey()
    assert spotifyApiKey is not None
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=spotifyApiKey
        )
    )
    SONGS = []
    playlist = sp.playlist(PLAYLIST_ID)
    results = playlist["tracks"]
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    print(len(tracks))
    for item in tracks:
        track = item.get("track")
        artistName = track.get("artists")[0].get("name")
        track = Track(
            name=track["name"],
            artist=artistName,
            spotify_id=track["id"],
            youtube_id="",
            popularity_score=track["popularity"],
            uploaded=False,
            blacklisted=False,
            coverURL=track['album']['images'][0]['url'],
            album_name=track['album']['name']
        )
        SONGS.append(track)
  
    return SONGS

def addSongsToDB(songs: List[Track]) -> None:
    for song in songs:
        addTrack(song)


if __name__ == "__main__":
    PLAYLIST_ID = "7Lg2IGZJGAvGYqqUEuvqkU"  # my playlist id
    SONGS = fetchPlaylistSongs(PLAYLIST_ID)
