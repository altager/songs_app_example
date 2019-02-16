from songs_app.errors import JsonHttpError


class InvalidQueryParameterError(JsonHttpError):
    def __init__(self):
        super().__init__(message='invalid_query_parameter', status_code=400)


class InvalidRequestParameterError(JsonHttpError):
    def __init__(self):
        super().__init__(message='invalid_request_parameter', status_code=400)


class InvalidJSONError(JsonHttpError):
    def __init__(self):
        super().__init__(message='invalid_json', status_code=400)
