from tinydb import TinyDB, Query
from Track import Track
db = TinyDB('db.json')
from typing import List 

def addTrack(track:Track):
    if(not doesTrackExist(track)):
        db.insert({"spotify_id":track.getSpotifyID(),"name":track.getName(),"artist":track.getArtist(),"popularity_score":track.getPopularityScore(),"uploaded":track.uploaded,"youtube_id":""})

def setTrackYoutubeID(track:Track,youtubeID:str):
    # Add youtube video ID to Track
    Track = Query()
    db.update({"youtube_id":youtubeID},Track["spotify_id"] == track["spotify_id"])


def setTrackUploadState(track,state:bool):
    Tracks = Query()
    db.update({"uploaded":state},Tracks["youtube_id"] == track["youtube_id"])


def doesTrackExist(track:Track) -> bool:
    Track = Query()
    result = db.search(Track["spotify_id"] ==track.getSpotifyID())
    return  len(result) >= 1

def getNewTracks() -> List[Track]:
    # returns unploadedTracks
    Track = Query()
    result = db.search(Track["uploaded"] == False)
    return result

if __name__ == "__main__":
    tracks = getNewTracks()
    print(tracks)