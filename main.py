from slow_reverb import slowReverb
from utils import setupDirectories,setupEnvironmentVariables,checkFFmpeg , MP4ToMP3
import moviepy.editor  as mp
from db import getNewTracks , setTrackUploadState , setTrackYoutubeID
from spotify import fetchPlaylistSongs , addSongsToDB
from youtube import Download , Search
from giphyapi import searchAndDownloadGif
import os

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
if(len(tracks) == 0):
    print("no song to upload , exiting.")
    quit()
from os.path import isfile, join
from os import listdir
def setupFilesPermissions():
    onlyfiles = [f for f in listdir(".") if isfile(join("./", f))]
    for file in onlyfiles:
        os.chmod(file , 0o777)




if("ON_HEROKU" in os.environ):
    setupFilesPermissions()

track = tracks[0]
print(track)
track_link , track_id = Search(track["name"] + " " + track["artist"])
if(track_link == ""):
    print("can't find youtube link , exiting.")
    quit()
print("downloading track from youtube")

Download(track_link)
print("converting to mp3")
MP4ToMP3("youtubeDownloads/song.mp4","song.mp3")
print("searching for gif ")
searchAndDownloadGif("anime")
print("applying slowed reverb")
slowReverb("song.mp3","gifs/originalGif.gif",slowRate=0.80)
print("post processing video")
video = mp.VideoFileClip("output/slowed-reverb.mp4")
black_image = (mp.ImageClip("black.jpg"))
final = mp.CompositeVideoClip([black_image, video.set_position("center").resize(height=768,width=768)])
final = final.set_start(0).set_duration(video.duration).resize(height=720,width=1280)
final.write_videofile("output/song.mp4")
print("starting upload")


songName = track["name"]+" - "+track["artist"]+ " (slowed & reverb)"
privacyStatus = "public"
description = ""
setTrackYoutubeID(track=track,youtubeID=track_id)

os.system(f'python upload_video.py --file "output/song.mp4" --title category="10" --title "{songName}" --description={description} --privacyStatus="{privacyStatus}" ')

print("done uploading , setting upload state to true")
setTrackUploadState(track,True)
