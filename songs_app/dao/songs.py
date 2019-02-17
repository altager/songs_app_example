import logging
import ujson as json

from songs_app.errors import DaoNotFound

logger = logging.getLogger(__name__)


class SongsDAO:
    def __init__(self, mongo_connection, cache_backend):
        self._mongo_connection = mongo_connection
        self._cache_backend = cache_backend

    def get_songs_list(self, limit=None, last_id=None):
        if last_id:
            songs_list = self._mongo_connection.songs.aggregate(
                [
                    {'$match': {'_id': {'$gt': last_id}}},
                    {'$project': {'_id': 0, 'id': {'$toString': '$_id'}, 'artist': 1, 'title': 1, 'difficulty': 1,
                                  'level': 1, 'released': 1}},
                    {'$limit': limit}
                ]
            )
        else:
            songs_list = self._mongo_connection.songs.aggregate(
                [
                    {'$project': {'_id': 0, 'id': {'$toString': '$_id'}, 'artist': 1, 'title': 1, 'difficulty': 1,
                                  'level': 1, 'released': 1}},
                    {'$limit': limit}
                ]
            )

        return list(songs_list)

    def get_average_difficulty(self, level=None):
        result = self._get_average_difficulty_from_cache(level=level)
        if not result:
            if level:
                result = list(self._get_average_difficulty_from_db(level=level))
                result = result[0] if result else {}
                if result:
                    self._cache_backend.upsert_value(
                        f'average_difficulty_{level}', value=json.dumps(result), expire_in=60
                    )
            else:
                result = list(self._get_average_difficulty_from_db())
                result = result[0] if result else {}
                if result:
                    self._cache_backend.upsert_value(
                        'average_difficulty_all', value=json.dumps(result), expire_in=60
                    )

        return result

    def _get_average_difficulty_from_db(self, level=None):
        if level:
            result = self._mongo_connection.songs.aggregate(
                [
                    {'$match': {'level': level}},
                    {'$group': {'_id': None, 'average_difficulty': {'$avg': '$difficulty'}}},
                    {'$project': {'_id': 0, 'level': {'$literal': level}, 'average_difficulty': 1}}
                ]
            )

        else:
            result = self._mongo_connection.songs.aggregate(
                [
                    {'$group': {'_id': None, 'average_difficulty': {'$avg': '$difficulty'}}},
                    {'$project': {'_id': 0, 'level': 'all', 'average_difficulty': 1}}
                ]
            )
        return result

    def _get_average_difficulty_from_cache(self, level=None):
        if level:
            cached_value = self._cache_backend.get_value(f'average_difficulty_{level}')
        else:
            cached_value = self._cache_backend.get_value(f'average_difficulty_all')

        return cached_value

    def search_songs(self, message):
        result = self._mongo_connection.songs.aggregate(
            [
                {'$match': {'$text': {'$search': message, '$caseSensitive': False}}},
                {'$project': {'_id': 0, 'id': {'$toString': '$_id'}, 'artist': 1, 'title': 1, 'difficulty': 1,
                              'level': 1, 'released': 1}},
            ]
        )

        return result

    def set_rating(self, song_id, rating):
        if not self._mongo_connection.songs.find_one({'_id': song_id}):
            raise DaoNotFound

        self._mongo_connection.songs_rating.insert_one(
            {'song_id': song_id, 'rating': rating}
        )

    def get_rating(self, song_id):
        if not self._mongo_connection.songs.find_one({'_id': song_id}):
            raise DaoNotFound

        result = self._get_song_rating_from_cache(song_id=str(song_id))
        if not result:
            result = list(self._get_song_rating_from_db(song_id=song_id))
            result = result[0] if result else {}
            if result:
                self._cache_backend.upsert_value(
                    f'song_rating_{str(song_id)}', value=json.dumps(result), expire_in=60
                )

        return result

    def _get_song_rating_from_db(self, song_id=None):
        if song_id:
            result = self._mongo_connection.songs_rating.aggregate(
                [
                    {'$match': {'song_id': song_id}},
                    {'$group': {'_id': None, 'avg_rating': {'$avg': '$rating'}, 'min': {'$min': '$rating'},
                                'max': {'$max': '$rating'}}},
                    {'$project': {'_id': 0, 'song_id': {'$toString': song_id}, 'avg_rating': 1, 'max': 1, 'min': 1}}
                ]
            )
        else:
            result = self._mongo_connection.songs_rating.aggregate(
                [
                    {'$group': {'_id': '$song_id', 'avg_rating': {'$avg': '$rating'}, 'min': {'$min': '$rating'},
                                'max': {'$max': '$rating'}}}
                ]
            )

        return result

    def _get_song_rating_from_cache(self, song_id):
        cached_value = self._cache_backend.get_value(f'song_rating_{song_id}')

        return cached_value
