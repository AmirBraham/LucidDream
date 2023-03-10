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
    print("fetching playlist songs")
    while True:
        while True:
            items = playlist.get("tracks").get("items")
            size = int(playlist["tracks"]["total"])
            for i in range(size):
                track = items[i].get("track")
                artistName = track.get("artists")[0].get("name")
                track = Track(
                    name=track["name"],
                    artist=artistName,
                    spotify_id=track["id"],
                    youtube_id="",
                    popularity_score=track["popularity"],
                    uploaded=False,
                    blacklisted=False
                )
                SONGS.append(track)

            if playlist.get("tracks").get("next") == None:
                break
            playlist["tracks"] = playlist.get("tracks").get("next")
        if playlist.get("next") == None:
            break
        playlist = playlist.get("next")
    return SONGS


def addSongsToDB(songs: List[Track]) -> None:
    for song in songs:
        addTrack(song)
