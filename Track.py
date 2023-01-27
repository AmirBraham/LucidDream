class Track:
    name = ""
    artist = ""
    spotify_id = ""
    isAlreadyProcessed = False
    popularity_score = 0
    youtubeID = ""

    def __init__(self, name, artist, spotify_id, popularity_score) -> None:
        self.name = name
        self.artist = artist
        self.spotify_id = spotify_id
        self.popularity_score = popularity_score

    def getName(self) -> str:
        return self.name

    def getArtist(self) -> str:
        return self.artist

    def getSpotifyID(self) -> str:
        return self.spotify_id

    def setYoutubeID(self,youtubeID) -> None:
        self.youtubeID = youtubeID
    def getYoutubeID(self) -> str:
        return self.youtubeID
    def getPopularityScore(self) -> int:
        return self.popularity_score

    def isAlreadyProcessed() -> bool:
        isAlreadyProcessed = True
        return isAlreadyProcessed

