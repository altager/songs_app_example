import requests
import pytest

from functests.test_utils.constants import URL_PREFIX
from functests.test_utils.response_validators import ErrorResponse


def test_set_song_rating(create_document):
    doc_id_1 = create_document({
        "artist": "Test Artist",
        "title": "hey",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })
    payload = {'song_id': str(doc_id_1), 'rating': 5}
    response = requests.post(
        URL_PREFIX + '/songs/rating',
        json=payload
    )

    assert response.status_code == 201


@pytest.mark.parametrize("rating", [-1, 0, 6, 0.1])
def test_set_song_rating_invalid_rating(rating):
    sample_id = '5c68837d51ef7ec66aa0c640'
    payload = {'song_id': sample_id, 'rating': rating}
    response = requests.post(
        URL_PREFIX + '/songs/rating',
        json=payload
    )

    assert response.status_code == 400
    error = ErrorResponse(**response.json())
    assert error.message == 'invalid_request_parameter'


def test_set_song_rating_song_not_found():
    sample_id = '000000000000000000000000'
    payload = {'song_id': sample_id, 'rating': 1}
    response = requests.post(
        URL_PREFIX + '/songs/rating',
        json=payload
    )

    assert response.status_code == 404
    error = ErrorResponse(**response.json())
    assert error.message == 'song_not_found'
