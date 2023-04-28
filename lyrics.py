
import lyricsgenius as lg
from utils import getGeniusKey
from Track import Track
import json

genius = lg.Genius(getGeniusKey(), skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=False)

def getAlbum(track:Track) -> str:
    album = genius.search_album(name=track["album_name"],artist=track["artist"]) 
    if(album == None):
        print(f"failed to get song lyrics for this track : {track} " )
        return
    album.save_lyrics("album",overwrite=True)


def lyricsCleanup(lyrics) -> str:
    lyrics = lyrics.split("\n")
    if("Translations" in  lyrics[0]):
        lyrics = lyrics[1:]
    lyrics[-1] = lyrics[-1].replace("1Embed","")
    return "\n".join(lyrics)


def getSongLyricsFromAlbum(track:Track) -> str:
    lyrics=""
    try:
        f = open("album.json")
        data = json.load(f)
        tracks = data["tracks"]
        lyrics = ""
        for t in tracks:
            if(t["song"]["title"] == track["name"]):
                lyrics = t["song"]["lyrics"]
        if(lyrics == ""):
            print("couldn't find song in album ")
            print(data)
            return ""
        lyrics = lyricsCleanup(lyrics=lyrics)
    except Exception as err:
        print(err)
        lyrics=""
    
    return lyrics


def getLyrics(track:Track) -> str:
    getAlbum(track=track) # saves all album songs to album.json
    lyrics = getSongLyricsFromAlbum(track=track) # reads album.json and gets song lyrics
    return lyrics
if __name__ == "__main__":
    exampleTrack = Track(name="RUNNING",artist="NF",album_name="HOPE")
    lyrics = getLyrics(track=exampleTrack )
    HASHTAGS = f'#slowed #reverb #{exampleTrack["artist"]}'
    DISCLAIMER="DISCLAIMER : We do not own ANY rights to any of the music or footage we share, if you have a problem with our way, shoot us an email : amirbrahamm@gmail.com, and your video will be removed from the youtube platform within 24 hours."
    d = [HASHTAGS]
    if(lyrics != ""):
        d.append(lyrics)
    d.append(DISCLAIMER)
    description = "\n".join(d)
    print(description)

