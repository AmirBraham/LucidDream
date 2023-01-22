
from pathlib import Path

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

def checkFFmpeg():
    try:
        import subprocess
        result = subprocess.run(['ffmpeg','-formats'], check=True, stdout=subprocess.PIPE)
        result = result.stdout
        #if we reached this line of code , it means success
        return True 
    except:
        print("ffmpeg not found, exiting..")
    return False
if __name__ == "__main__":
    checkFFmpeg()