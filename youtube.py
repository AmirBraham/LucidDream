from pytube import YouTube

from youtubesearchpython import VideosSearch
from Track import Track

def Search(title:Track,i):
    limit = 5
    if(i > limit):
        raise Exception("i is bigger than limit")

    videosSearch = VideosSearch(title, limit = limit)
    result = videosSearch.result()["result"]

    if(len(result) > 0):
        return result[i]["link"] , result[i]["id"]
    return ""




def Download(link,title):
    try:
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_audio_only()
        youtubeObject.download("youtubeDownloads","song.mp4")
    except:
        print("An error has occurred , trying another link")
        link = Search(title,1)[0]
        Download(link=link,title=title)
    print("Download is completed successfully")


