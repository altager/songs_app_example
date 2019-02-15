class SongsDAO:
    def __init__(self, mongo_connection):
        self._mongo_connection = mongo_connection

    def get_songs_list(self, limit=None, last_id=None):
        # TODO: refactor
        if last_id:
            # this approach is a much faster than skip/limit
            songs_list = self._mongo_connection.songs.find({'_id': {'$gt': last_id}}).limit(limit)
        else:
            songs_list = self._mongo_connection.songs.find({}).limit(limit)
        return list(songs_list)
