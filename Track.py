class Track:
    name = ""
    artist = ""
    spotify_id = ""
    popularity_score = 0
    youtube_id = ""
    uploaded = False

    def __init__(
        self, name, artist, spotify_id, youtube_id, popularity_score, uploaded=False
    ) -> None:
        self.name = name
        self.artist = artist
        self.spotify_id = spotify_id
        self.youtube_id = youtube_id
        self.popularity_score = popularity_score
        self.uploaded = uploaded

    def getName(self) -> str:
        return self.name

    def getArtist(self) -> str:
        return self.artist

    def getSpotifyID(self) -> str:
        return self.spotify_id

    def setYoutubeID(self, youtube_id) -> None:
        self.youtube_id = youtube_id

    def getYoutubeID(self) -> str:
        return self.youtube_id

    def getPopularityScore(self) -> int:
        return self.popularity_score
    def __str__(self) -> str:
        return f"""
        Track Details : \n
        Name : {self.getName()} \n
        Artist : {self.getArtist()} \n
        Youtube link : https://www.youtube.com/watch?v={self.getYoutubeID()} \n
        Spotify Link : https://open.spotify.com/track/{self.getSpotifyID()} \n
        Popularity Score : {self.getPopularityScore()}
        """
