from songs_app.dao import SongsDAO
from songs_app.errors import DaoNotFound, SongNotFoundError
from songs_app.utils import json_response
from songs_app.validators.query import query_validator, GetLimitLastId, GetLevel, Search
from songs_app.validators.request import request_validator, CreateRating


class SongsHandler:
    def __init__(self, songs_dao: SongsDAO):
        self._songs_dao = songs_dao

    @query_validator(GetLimitLastId)
    def get_songs_list(self, query_data: GetLimitLastId):
        songs_list = self._songs_dao.get_songs_list(limit=query_data.limit, last_id=query_data.last_id)
        return json_response(songs_list)

    @query_validator(GetLevel)
    def get_avg_difficulty(self, query_data: GetLevel):
        avg_difficulty = self._songs_dao.get_average_difficulty(level=query_data.level)
        return json_response(avg_difficulty)

    @query_validator(Search)
    def search_songs(self, query_data: Search):
        search_result = self._songs_dao.search_songs(message=query_data.message)
        return json_response(search_result)

    @request_validator(CreateRating)
    def set_rating(self, query_data: CreateRating):
        try:
            self._songs_dao.set_rating(song_id=query_data.song_id, rating=query_data.rating)
        except DaoNotFound:
            raise SongNotFoundError
        return json_response(b'', 201)

    def get_song_rating(self, song_id):
        try:
            result = self._songs_dao.get_rating(song_id=song_id)
        except DaoNotFound:
            raise SongNotFoundError

        return json_response(result)
