import ujson as json
from datetime import datetime

from bson import ObjectId
from werkzeug.wrappers import Response


class JSONHttpResponse(Response):
    """
    Custom class for json http response
    """

    def __init__(self, response=None, status=None):
        super().__init__(response=response, content_type='application/json', status=status)


# wrapper function for JSONHttpResponse
def json_response(data):
    def _process_doc(data):
        if isinstance(data, dict):
            for key in data:
                val = data[key]
                if isinstance(val, ObjectId) or isinstance(val, datetime):
                    data[key] = str(val)

    if isinstance(data, list):
        for doc in data:
            _process_doc(doc)

    if isinstance(data, dict):
        _process_doc(data)

    # possibly we can get already dumped bytes from redis. so we dont need to dump them again
    if not isinstance(data, bytes):
        data = json.dumps(data)

    return JSONHttpResponse(data)
