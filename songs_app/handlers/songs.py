from songs_app.db.dao import SongsDAO
from songs_app.utils import json_response
from songs_app.validators.query import query_validator, GetLimitLastId


class SongsHandler:
    def __init__(self, songs_dao: SongsDAO):
        self.songs_dao = songs_dao

    @query_validator(GetLimitLastId)
    def get_songs_list(self, query_data: GetLimitLastId):
        songs_list = self.songs_dao.get_songs_list(limit=query_data.limit, last_id=query_data.last_id)
        return json_response(songs_list)

    def get_difficulty(self):
        pass

    def search_songs(self):
        pass

    def set_rating(self):
        pass

    def get_song_rating(self):
        pass
