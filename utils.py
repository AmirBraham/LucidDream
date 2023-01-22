from dotenv import load_dotenv
import os
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


