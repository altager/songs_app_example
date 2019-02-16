from urllib.parse import urlencode

import requests

from functests.test_utils.constants import URL_PREFIX
from functests.test_utils.response_validators import SongResponse


def test_songs_search_artist(cleanup_db, create_document):
    doc_id_1 = create_document({
        "artist": "Test Artist",
        "title": "hey",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    doc_id_2 = create_document({
        "artist": "Test artist Mega",
        "title": "yo",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    create_document({
        "artist": "Any other",
        "title": "thx",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    response = requests.get(URL_PREFIX + '/songs/search?' + urlencode({'message': 'test artist'}))

    assert response.status_code == 200
    songs_response_ids = [SongResponse(**doc).id for doc in response.json()]
    assert len(songs_response_ids) == 2
    assert [doc_id_1, doc_id_2] == sorted(songs_response_ids)


def test_songs_search_title(cleanup_db, create_document):
    create_document({
        "artist": "Test Artist",
        "title": "thx",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    doc_id_2 = create_document({
        "artist": "Test artist Mega",
        "title": "yo",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    doc_id_3 = create_document({
        "artist": "Any other",
        "title": "man yo",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    response = requests.get(URL_PREFIX + '/songs/search?' + urlencode({'message': 'YO'}))

    assert response.status_code == 200
    songs_response_ids = [SongResponse(**doc).id for doc in response.json()]
    assert len(songs_response_ids) == 2
    assert [doc_id_2, doc_id_3] == sorted(songs_response_ids)
