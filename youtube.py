from pytube import YouTube
from youtubesearchpython import VideosSearch
from Track import Track

def Search(title: Track, videoIndex : int = 0):
    limit = 5
    if videoIndex > limit:
        raise Exception("max retries number exceeded")

    videosSearch = VideosSearch(title, limit=limit)
    result = videosSearch.result()["result"]

    if len(result) > 0:
        return result[videoIndex]["link"], result[videoIndex]["id"]
    return []


def Download(link:str, title:str) -> bool:
    try:
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_audio_only()
        youtubeObject.download("youtubeDownloads", "song.mp4")
        print("Download is completed successfully")
        return True
    except:
        print("An error has occurred , trying another link")
        newlink = Search(title, 1)[0]
        if(link is not None and newlink != link):
            Download(link=link, title=title)
        else:
            print("failed to find youtube link for spotify song : " + title)
            print("proceding to remove spotify song from playlist as to not cause failure on every startup")
            return False
    return False