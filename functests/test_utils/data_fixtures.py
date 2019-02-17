import pytest
import requests

from functests.test_utils.constants import URL_PREFIX

__all__ = [
    'create_document',
    'set_song_rating'
]


@pytest.fixture
def create_document(db):
    def _create_document(data: dict):
        return str(db.songs.insert_one(data).inserted_id)

    return _create_document


@pytest.fixture
def set_song_rating():
    def _set_song_rating(song_id: str, rating: int):
        payload = {'song_id': song_id, 'rating': rating}
        requests.post(
            URL_PREFIX + '/songs/rating',
            json=payload
        )

    return _set_song_rating
