import requests

from functests.test_utils.constants import URL_PREFIX
from functests.test_utils.response_validators import AvgRatingResponse, ErrorResponse


def test_get_song_rating(create_document, set_song_rating):
    doc_id = create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 8,
        "level": 10,
        "released": "2016-10-26"
    })
    set_song_rating(doc_id, 2)
    set_song_rating(doc_id, 4)
    set_song_rating(doc_id, 3)

    response = requests.get(URL_PREFIX + f'/songs/avg/rating/{doc_id}')

    assert response.status_code == 200
    song_rating = AvgRatingResponse(**response.json())

    assert doc_id == song_rating.song_id
    assert (2 + 4 + 3) / 3 == song_rating.avg_rating
    assert 2 == song_rating.min
    assert 4 == song_rating.max


def test_get_song_rating_song_not_found():
    song_id = '000000000000000000000000'

    response = requests.get(URL_PREFIX + f'/songs/avg/rating/{song_id}')

    assert response.status_code == 404
    error = ErrorResponse(**response.json())
    assert error.message == 'song_not_found'


def test_get_song_rating_empty_rating(create_document):
    doc_id = create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 8,
        "level": 10,
        "released": "2016-10-26"
    })

    response = requests.get(URL_PREFIX + f'/songs/avg/rating/{doc_id}')

    assert response.status_code == 200
    assert response.json() == {}
