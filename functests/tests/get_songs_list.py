from urllib.parse import urlencode

import requests

from functests.test_utils.constants import URL_PREFIX
from functests.test_utils.helpers import replace_id
from functests.test_utils.response_validators import Song


def test_get_songs_list():
    response = requests.get(URL_PREFIX + '/songs')

    assert response.status_code == 200
    # check default limit
    assert len(response.json()) == 5
    [Song(**replace_id(doc)) for doc in response.json()]


def test_get_songs_list_limit():
    response = requests.get(URL_PREFIX + '/songs?' + urlencode({'limit': 1}))

    assert response.status_code == 200
    assert len(response.json()) == 1

    Song(**replace_id(response.json()[0]))


def test_get_songs_list_offset_with_last_id():
    songs_response = requests.get(URL_PREFIX + '/songs').json()
    first_song = Song(**replace_id(songs_response[0]))

    songs_response_after_offset = requests.get(
        URL_PREFIX + '/songs?' + urlencode({'last_id': str(first_song.id)})
    ).json()

    assert songs_response[1:] == songs_response_after_offset[:-1]


def test_get_songs_list_limit_offset_with_last_id():
    songs_response = requests.get(URL_PREFIX + '/songs').json()
    first_song = Song(**replace_id(songs_response[0]))

    songs_response_after_offset = requests.get(
        URL_PREFIX + '/songs?' + urlencode({'last_id': str(first_song.id), 'limit': 1})
    ).json()

    assert songs_response[1] == songs_response_after_offset[0]
