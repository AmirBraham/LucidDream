from pytube import YouTube

from youtubesearchpython import VideosSearch
videosSearch = VideosSearch('HAKAI - Cicatrices', limit = 2)
print(videosSearch.result()["result"][0]["link"])


def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


#link = input("Enter the YouTube video URL: ")
#Download(link)