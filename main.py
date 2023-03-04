import random
from slowedreverb import slowReverb
from utils import setupDirectories, setupEnvironmentVariables, checkFFmpeg, MP4ToMP3
from db import getNewTracks, setTrackUploadState, setTrackYoutubeID, updateDB
from spotify import fetchPlaylistSongs, addSongsToDB
from youtube import Download, Search
import os
from os.path import isfile, join


updateDB()
print("setting up directories")
setupDirectories()
if not ("ON_HEROKU" in os.environ):
    setupEnvironmentVariables()
    assert checkFFmpeg()
print("found ffmpeg , starting process")
PLAYLIST_ID = "7Lg2IGZJGAvGYqqUEuvqkU"  # my playlist id

print("fetching playlist songs")
SONGS = fetchPlaylistSongs(PLAYLIST_ID)
addSongsToDB(SONGS)
tracks = getNewTracks()
if len(tracks) == 0:
    print("no song to upload , exiting.")
    quit()



def setupFilesPermissions():
    onlyfiles = [f for f in os.listdir(".") if isfile(join("./", f))]
    for file in onlyfiles:
        os.chmod(file, 0o777)


if "ON_HEROKU" in os.environ:
    setupFilesPermissions()

track = tracks[0]
track_link, track_id = Search(track["name"] + " " + track["artist"], 0)
if track_link == "":
    print("can't find youtube link , exiting.")
    quit()
print("downloading track from youtube")

Download(track_link, title=track["name"] + " " + track["artist"])
track["youtube_id"] = track_id
print("converting to mp3")
MP4ToMP3("youtubeDownloads/song.mp4", "song.mp3")
print("searching for gif ")
print("applying slowed reverb")

print("post processing video")


random_file=random.choice(os.listdir("gifs"))
slowReverb(
    audio="./song.mp3",
    output="./output/slowed-reverb.mp4",
    gif_path="./gifs/"+random_file,
)
quit()

songName = track["name"] + " - " + track["artist"] + " (slowed & reverb)"
privacyStatus = "public"
description = ""

setTrackYoutubeID(track=track, youtubeID=track_id)
print("starting upload")
os.system(
    f'python upload_video.py --file "./output/slowed-reverb.mp4"  --category="10" --title "{songName}" --description={description} --privacyStatus="{privacyStatus}" '
)
uploadState = setTrackUploadState(track, True)
if uploadState:
    print("done uploading , setting upload state to true")
    print("Done !  added the following track : \n")
    print(
        f"""
            Track Details : \n
            Name : {track["name"]} \n
            Artist : {track["artist"]} \n
            Youtube link : https://www.youtube.com/watch?v={track["youtube_id"]} \n
            Spotify Link : https://open.spotify.com/track/{track["spotify_id"]} \n
            Popularity Score : {track["popularity_score"]}
            """
    )
