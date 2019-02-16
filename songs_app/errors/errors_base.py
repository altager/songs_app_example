from werkzeug.exceptions import HTTPException

from songs_app.utils import json_response


class JsonHttpError(HTTPException):
    def __init__(self, message, status_code):
        super().__init__(self, response=json_response({'message': message}, status=status_code))
