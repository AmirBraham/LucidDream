from pytube import YouTube

from youtubesearchpython import VideosSearch
from Track import Track

def Search(title:Track):
    videosSearch = VideosSearch(title, limit = 2)
    result = videosSearch.result()["result"]

    if(len(result) > 0):
        return result[0]["link"] , result[0]["id"]
    return ""




def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download("youtubeDownloads","song.mp4")
    except:
        print("An error has occurred")
    print("Download is completed successfully")


