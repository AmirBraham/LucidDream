import random
from slowedreverb import slowReverb
from utils import setupDirectories, setupEnvironmentVariables, checkFFmpeg, MP4ToMP3, setupFilesPermissions,generateYoutubeClientSecret
from db import setUpDatabase, getNewTrack, blacklistTrack
from spotify import fetchPlaylistSongs, addSongsToDB
from youtube import Download, Search
import os
from upload_video import upload
import subprocess as sp

if not ("ON_HEROKU" in os.environ):
    setupEnvironmentVariables()
    assert checkFFmpeg()
    setupFilesPermissions()

setUpDatabase()
PLAYLIST_ID = "7Lg2IGZJGAvGYqqUEuvqkU"  # my playlist id
SONGS = fetchPlaylistSongs(PLAYLIST_ID)
addSongsToDB(SONGS)
track = getNewTrack()
if track == None:
    print("no song to upload , exiting.")
    quit()
setupDirectories()

track_link, track_id = Search(track["name"] + " " + track["artist"], 0)
if track_link == "":
    print("can't find youtube link , exiting.")
    quit()
print("downloading track from youtube")
downloadStatus = Download(
    track_link, title=track["name"] + " " + track["artist"])
if(not downloadStatus):
    blacklistTrack(track)
    quit()
print("searching for gif ")
print("applying slowed reverb")
print("post processing video")

random_file = random.choice(os.listdir("gifs"))
slowReverb(
    audio="./song.mp3",
    output="./output/slowed-reverb.mp4",
    gif_path="./gifs/"+random_file,
)

songName = track["name"] + " - " + track["artist"] + " (slowed & reverb)"
privacyStatus = "public"
description = ""

print("starting upload")
if("ON_HEROKU" in os.environ):
    generateYoutubeClientSecret("client_secrets.json")
    generateYoutubeClientSecret("main.py-oauth2.json")


print("preparing mp4 video for youtube")
sp.call('ffmpeg -i ./output/slowed-reverb.mp4 -c:v libx264  -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -preset slow -crf 18 -c:a copy -pix_fmt yuv420p ./output/final.mp4',shell=True)

upload(track=track,title=songName,filename="./output/final.mp4",category="10",description=description,privacyStatus="public")

