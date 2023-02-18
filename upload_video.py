from youtube_upload.client import YoutubeUploader

uploader = YoutubeUploader()
uploader.authenticate()

# Video options
options = {
    "title": "Example title",  # The video title
    "description": "Example description",  # The video description
    "tags": ["tag1", "tag2", "tag3"],
    "categoryId": "22",
    "privacyStatus": "private",  # Video privacy. Can either be "public", "private", or "unlisted"
    "kids": False,  # Specifies if the Video if for kids or not. Defaults to False.
}

# upload video
uploader.upload("sample.mp4", options)
