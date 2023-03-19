from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
import yt_dlp
from Track import Track


def Search(title: Track, videoIndex: int = 0):
    limit = 5
    if videoIndex > limit:
        raise Exception("max retries number exceeded")

    videosSearch = VideosSearch(title, limit=limit)
    result = videosSearch.result()["result"]

    if len(result) > 0:
        return result[videoIndex]["link"], result[videoIndex]["id"]
    return []


def Download(link: str, title: str) -> bool:
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'outtmpl':"song"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([link])
            print(error_code)
        
        print("Download is completed successfully")
        if(error_code != 0):
            raise Exception("trying new link " )
        return True
    except Exception as err:
        print("err : \n")
        print(err)
        print("\n")
        newlink = Search(title, 1)[0]
        if(link is not None and newlink != link):
            print("new link : " + newlink)
            Download(link=link, title=title)
        else:
            print("failed to find youtube link for spotify song : " + title)
            print(
                "proceding to remove spotify song from playlist as to not cause failure on every startup")
            return False
    return False
