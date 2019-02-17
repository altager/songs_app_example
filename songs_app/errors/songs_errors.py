from songs_app.errors import JsonHttpError


class SongNotFoundError(JsonHttpError):
    def __init__(self):
        super().__init__(message="song_not_found", status_code=404)
