from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
import yt_dlp
from Track import Track


def Search(title: Track):
    videosSearch = VideosSearch(title, limit=1)
    result = videosSearch.result()["result"]
    if len(result) > 0:
        return result[0]["link"], result[0]["id"]
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
            'outtmpl': "song"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([link])
            print(error_code)
        print("Download is completed successfully")
        if(error_code != 0):
            raise Exception("trying new link ")
        return True
    except Exception as err:
        print("err : \n")
        print(err)
        print("\n")
        print("failed to find youtube link for spotify song : " + title)
    return False
