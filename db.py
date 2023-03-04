from tinydb import TinyDB, Query
from Track import Track
from typing import List


db = TinyDB("db.json")


def addTrack(track: Track):
    if not doesTrackExist(track):
        db.insert(
            {
                "spotify_id": track.getSpotifyID(),
                "name": track.getName(),
                "artist": track.getArtist(),
                "popularity_score": track.getPopularityScore(),
                "uploaded": track.uploaded,
                "youtube_id": "",
            }
        )


def setTrackYoutubeID(track: Track, youtubeID: str):
    # Add youtube video ID to Track
    Track = Query()
    db.update({"youtube_id": youtubeID}, Track["spotify_id"] == track["spotify_id"])


def setTrackUploadState(track, state: bool):
    if(not "youtube_id" in track):
        print("can't change upload state , probably failed to upload due to 'quota exceeded' reasons")
        return
    Tracks = Query()
    db.update({"uploaded": state}, Tracks["youtube_id"] == track["youtube_id"])
    return True

def doesTrackExist(track: Track) -> bool:
    Track = Query()
    result = db.search(Track["spotify_id"] == track.getSpotifyID())
    return len(result) >= 1


def getNewTracks() -> List[Track]:
    # returns unploadedTracks
    Track = Query()
    result = db.search(Track["uploaded"] == False)
    return result

def updateDB():
    Track = Query()
    # setting upload state to true for tracks with youtube_id 
    res = db.search((Track["youtube_id"] != "") & (Track["uploaded"] == False))
    for track in res:
        setTrackUploadState(track=track,state=True)
    #removing tracks with uploaded state true and youtube id none
    Track = Query()
    db.remove((Track["youtube_id"] == "") & (Track["uploaded"] == True))
    
if __name__ == "__main__":
    updateDB()
