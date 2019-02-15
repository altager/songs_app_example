import requests

from functests.test_utils.constants import URL_PREFIX


def test_get_songs_list():
    response = requests.get(URL_PREFIX + '/songs')

    assert response.status_code == 200
    assert len(response.json()) == 11
