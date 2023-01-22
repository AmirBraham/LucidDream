import giphy_client
from giphy_client.rest import ApiException
from random import randint
import urllib.request
from utils import getGiphyApiKey


def searchDownloadGif(q, limit=10, offset=0):
    api_instance = giphy_client.DefaultApi()
    api_key = getGiphyApiKey("")
    if api_key == False:
        print("api key not valid")
        return
    try:
        api_response = api_instance.gifs_search_get(
            api_key, q, limit=limit, offset=offset
        )
        extractGif(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


def extractGif(api_response):
    if api_response.data == None:
        print("no response")
        return
    data = api_response.data
    processedData = []
    for gif in data:
        if gif.images.original.width == gif.images.original.height:
            processedData.append(gif)
    if len(processedData) < 2:
        print("not found")
        return
    index = randint(0, len(processedData) - 1)
    originalGif = processedData[index].images.original
    urllib.request.urlretrieve(originalGif.url, "gifs/originalGif.gif")


if __name__ == "__main__":
    searchDownloadGif("smoke")
