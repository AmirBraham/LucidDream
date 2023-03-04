import json
from dotenv import load_dotenv
import os
from pathlib import Path
import subprocess
from moviepy.editor import *
from os.path import isfile, join


def checkFFmpeg():
    try:
        result = subprocess.run(
            ["ffmpeg", "-formats"], check=True, stdout=subprocess.PIPE
        )
        result = result.stdout
        # if we reached this line of code , it means success
        print("found ffmpeg , starting process")
        return True
    except:
        print("ffmpeg not found, exiting..")

    return False


def checkDATABASE():
    assert os.path.isfile("./db") == True, "database file not found"
    f = open("db", "r")
    return f.read()


# API KEYS CHECK
envPath = Path(".env")


def setupEnvironmentVariables():

    mongoDBkey = ""
    spotifyApiKey = ""
    youtubeApiKey = ""

    if not envPath.is_file():
        print(".env does not exist , do you wish to create one ? y/n \n")
        choice = input("")
        if choice.upper() != "Y":
            return False
        spotifyApiKey = input("Please choose spotify api key : \n")
        youtubeApiKey = input("Please choose youtube api key : \n")
        mongoDBkey = input("Please choose mongodb key : \n")
        f = open(".env", "a")
        f.writelines(
            '\n'.join(
                [
                    'MONGO_DB=' + mongoDBkey,
                    'YOUTUBE_SECRET=' + youtubeApiKey,
                    'SPOTIPY_CLIENT_SECRET=' + spotifyApiKey,
                ]) + '\n'
        )


load_dotenv()


def getSpotifyApiKey(key=""):
    if(key != ""):
        return key
    api_key = os.environ.get("SPOTIPY_CLIENT_SECRET")
    return api_key


def getMongoDBKey(key=""):
    if key == "" or key == None:
        api_key = os.environ.get("MONGO_DB")
        if api_key is not None:
            return api_key
    result = key if key != "" else False
    return result


def setupDirectories():
    print("setting up directories")
    try:
        os.makedirs("output")
    except FileExistsError:
        # directory already exists
        pass
    try:
        os.makedirs("gif")
    except FileExistsError:
        # directory already exists
        pass


def generateYoutubeClientSecret(filename):
    f = open(filename)
    data = json.load(f)
    if("web" in data):
        data["web"]["client_secret"] = os.environ.get("YOUTUBE_SECRET")
    else:
        data["client_secret"] = os.environ.get("YOUTUBE_SECRET")
    with open(filename, "w") as outfile:
        outfile.write(json.dumps(data))
    f.close()


def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()
    os.remove(mp4)


def setupFilesPermissions():
    onlyfiles = [f for f in os.listdir(".") if isfile(join("./", f))]
    for file in onlyfiles:
        os.chmod(file, 0o777)


if __name__ == "__main__":
    generateYoutubeClientSecret()
