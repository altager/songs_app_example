from urllib.parse import urlencode

import requests

from functests.test_utils.constants import URL_PREFIX
from functests.test_utils.response_validators import SongResponse


def test_get_songs_list(cleanup_db, create_document):
    create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })
    response = requests.get(URL_PREFIX + '/songs')

    assert response.status_code == 200
    assert len(response.json()) == 1
    [SongResponse(**doc) for doc in response.json()]


def test_get_songs_list_limit(cleanup_db, create_document):
    doc_id_1 = create_document({
        "artist": "Test artist1",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })
    create_document({
        "artist": "Test artist2",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })
    response = requests.get(URL_PREFIX + '/songs?' + urlencode({'limit': 1}))

    assert response.status_code == 200
    assert len(response.json()) == 1

    song_response = SongResponse(**response.json()[0])
    assert song_response.id == doc_id_1


def test_get_songs_list_offset_with_last_id(cleanup_db, create_document):
    doc_id_1 = create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })
    doc_id_2 = create_document({
        "artist": "Test artist2",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })
    doc_id_3 = create_document({
        "artist": "Test artist3",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    response = requests.get(
        URL_PREFIX + '/songs?' + urlencode({'last_id': doc_id_1})
    )
    songs_response_ids_after_offset = [SongResponse(**doc).id for doc in response.json()]
    assert [doc_id_2, doc_id_3] == songs_response_ids_after_offset


def test_get_songs_list_limit_offset_with_last_id(cleanup_db, create_document):
    doc_id_1 = create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })
    doc_id_2 = create_document({
        "artist": "Test artist2",
        "title": "test",
        "difficulty": 10,
        "level": 10,
        "released": "2016-10-26"
    })

    response = requests.get(
        URL_PREFIX + '/songs?' + urlencode({'last_id': str(doc_id_1), 'limit': 1})
    )

    assert doc_id_2 == SongResponse(**response.json()[0]).id
