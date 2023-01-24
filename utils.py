from dotenv import load_dotenv
import os
from pathlib import Path
import subprocess






def checkFFmpeg():
    try:
        result = subprocess.run(['ffmpeg','-formats'], check=True, stdout=subprocess.PIPE)
        result = result.stdout
        #if we reached this line of code , it means success
        return True 
    except:
        print("ffmpeg not found, exiting..")
    return False


def checkDATABASE():
    assert os.path.isfile("./db") == True , "database file not found"
    f = open("db","r")
    return f.read()
# API KEYS CHECK
envPath = Path("./env")

def checkEnvironmentVariables():
    giphyApikey = ""
    spotifyApiKey = ""
    youtubeApiKey = ""
    if(not envPath.is_file()):
        print(".env does not exist , do you wish to create one ? y/n \n")
        choice = input("")
        if(choice.upper() != "Y"):
            return False
        spotifyApiKey = input("Please choose spotify api key : \n")
        youtubeApiKey = input("Please choose youtube api key : \n")
        giphyApikey = input("Please choose giphy api key : \n")
        f = open(".env","a")
        f.writelines(["giphy_api="+giphyApikey,"\nyoutube_api="+youtubeApiKey,"\nspotify_api="+spotifyApiKey])



load_dotenv()
def getSpotifyApiKey(key = ""):
    if(key == ""):
        api_key = os.environ.get("spotify_api")
        if(api_key != None):
            return api_key
    result = key if key != "" else False
    return  result



def getGiphyApiKey(key = ""):
    if(key == ""):
        api_key = os.environ.get("giphy_api")
        if(api_key != None):
            return api_key
    result = key if key != "" else False
    return  result

def setupDirectories():
    try:
        os.makedirs("gifs")
    except FileExistsError:
        # directory already exists
        pass
    try:
        os.makedirs("output")
    except FileExistsError:
        # directory already exists
        pass


