from songs_app.errors import JsonHttpError


class InvalidQueryParameter(JsonHttpError):
    def __init__(self):
        super().__init__(message='invalid_query_parameter', status_code=400)
