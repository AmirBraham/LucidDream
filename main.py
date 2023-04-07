import random
from slowedreverb import slowReverb
from utils import setupDirectories, setupEnvironmentVariables,resizeImage, checkFFmpeg, MP4ToMP3,downloadImage, setupFilesPermissions,generateYoutubeClientSecret
from db import setUpDatabase, getNewTrack, blacklistTrack
from spotify import fetchPlaylistSongs, addSongsToDB
from youtube import Download, Search
import os
from upload_video import upload
import subprocess as sp
from lyrics import getLyrics
if not ("ON_HEROKU" in os.environ):
    setupEnvironmentVariables()
    assert checkFFmpeg()
    setupFilesPermissions()

setUpDatabase()
PLAYLIST_ID = "7Lg2IGZJGAvGYqqUEuvqkU"  # my playlist id
SONGS = fetchPlaylistSongs(PLAYLIST_ID)
addSongsToDB(SONGS)
track = getNewTrack()
print(track)
if track == None:
    print("no song to upload , exiting.")
    quit()
setupDirectories()

track_link, track_id = Search(track["name"] + " " + track["artist"])
if track_link == "":
    print("can't find youtube link , exiting.")
    quit()
print("downloading track from youtube")
downloadStatus = Download(
    track_link, title=track["name"] + " " + track["artist"])

if(not downloadStatus):
    blacklistTrack(track)
    quit()

print("fetching Image ")
downloadImage(track["coverURL"]) # saves image as img.jpg
resizeImage("img.jpg",factor=1.2)
print("applying slowed reverb")
print("post processing video")
random_file = random.choice(os.listdir("gifs"))
slowReverb(
    audio="./song.mp3",
    output="./output/slowed-reverb.mp4",
    imagePath="output.jpg",
)

songName = track["name"] + " - " + track["artist"] + " (slowed & reverb)"
privacyStatus = "public"
lyrics = getLyrics(track=track)

HASHTAGS = f'#slowed #reverb #{track["artist"]}'
DISCLAIMER="DISCLAIMER : We do not own ANY rights to any of the music or footage we share, if you have a problem with our way, shoot us an email : amirbrahamm@gmail.com, and your video will be removed from the youtube platform within 24 hours."
d = [HASHTAGS]
if(lyrics != ""):
    d.append("LYRICS : \n" + lyrics + "\n")
d.append(DISCLAIMER)
description = "\n".join(d)

print("starting upload")
if("ON_HEROKU" in os.environ):
    generateYoutubeClientSecret("client_secrets.json")
    generateYoutubeClientSecret("main.py-oauth2.json")

print("preparing mp4 video for youtube")
sp.call('ffmpeg -i ./output/slowed-reverb.mp4 -c:v libx264  -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -preset slow -crf 18 -c:a copy -pix_fmt yuv420p ./output/final.mp4',shell=True)
upload(track=track,title=songName,filename="./output/final.mp4",category="10",description=description,privacyStatus="public")

