class SongsDAO:
    def __init__(self, mongo_connection):
        self._mongo_connection = mongo_connection
