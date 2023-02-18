from tinydb import TinyDB, Query
from Track import Track
db = TinyDB('db.json')

def addTrack(track:Track):
    if(not doesTrackExist(track)):
        db.insert({"spotify_id":track.getSpotifyID,"name":track.getName,"artist":track.getArtist,"popularity_score":track.getPopularityScore})

def setTrackYoutubeID(track:Track,youtubeID:str):
    # Add youtube video ID to Track
    Track = Query()
    db.update({"youtube_id":youtubeID},Track["spotify_id"] == track.spotify_id)


def setTrackUploadState(track:Track,state:bool):
    if(track.getYoutubeID() == ""):
        raise Exception("missing youtube id !")
    Tracks = Query()
    db.update({"uploaded":state},Tracks["youtube_id"] == track.getYoutubeID())


def doesTrackExist(track:Track):
    Track = Query()
    result = db.search(Track["spotify_id"] ==track.getSpotifyID)
    return  len(result) > 1

def getNewTracks():
    # returns unploadedTracks
    Track = Query()
    result = db.search(Track["uploaded"] == False)
    return result