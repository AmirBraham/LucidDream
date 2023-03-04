from typing import TypedDict
class Track(TypedDict):
    name : str
    artist : str
    spotify_id : str
    popularity_score : int
    youtube_id : str
    uploaded : bool
    blacklisted:bool
