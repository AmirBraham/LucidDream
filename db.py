from Track import Track
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.results import UpdateResult
from utils import getMongoDBKey
from os import environ


def connectToDB(username: str, password: str) -> Collection:
    client: MongoClient = MongoClient(
        f"mongodb+srv://{username}:{password}@songs.oexwbqj.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db: Collection = client["songs"]["songs"]
    return db


collection: Collection[Track] = None


def doesTrackExist(track: Track) -> bool:
    return collection.count_documents({"spotify_id": track.getSpotifyID()}, limit=1) != 0


def addTrack(track: Track) -> None:
    if not doesTrackExist(track):
        collection.insert_one(track.toDict())


def setTrackYoutubeID(track: Track, youtubeID: str) -> bool:
    # Add youtube video ID to Track
    res: UpdateResult = collection.update_one({'youtube_id': track['youtube_id']}, {
                                              '$set': {'spotify_id': track['spotify_id']}})
    return res.matched_count == 1


def setTrackUploadState(track, state: bool) -> bool:
    if(not "youtube_id" in track):
        print("can't change upload state , probably failed to upload due to 'quota exceeded' reasons")
        return
    res: UpdateResult = collection.update_one(
        {'youtube_id': track['youtube_id']}, {'$set': {'uploaded': state}})
    return res.matched_count == 1


def getNewTrack() -> Track:
    # returns unploadedTracks
    query = {'uploaded' == False , 'blacklisted' == False}
    result = collection.find_one(filter=query)
    return result


def setUpDatabase() -> None:
    print("connecting to mongodb database")
    collection = connectToDB("root", getMongoDBKey(environ.get('MONGO_DB')))
    # gte : greater than or equal to len(' ')
    query = {'youtube_id': {'$gte': ' '}, 'uploaded': False}
    # setting upload state to true for tracks with youtube_id
    res = collection.find(query)
    for track in res:
        setTrackUploadState(track=track, state=True)

    # removing tracks with uploaded state true and youtube id none
    filterTracks = {'youtube_id': '', 'uploaded': True}
    collection.delete_many(filter=filterTracks)


def blacklistTrack(track: Track) -> None:
    # gte : greater than or equal to len(' ')
    query = {'spotify_id': track['spotify_id']}
    track = collection.find_one_and_update(
        filter=query, update={'$set': {"blacklisted": True}})

if __name__ == "__main__":
    collection = connectToDB("root", "4Xstr48OJNx2wBwY")
    setUpDatabase()
