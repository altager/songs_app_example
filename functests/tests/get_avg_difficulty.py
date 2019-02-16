from urllib.parse import urlencode

import requests

from functests.test_utils.constants import URL_PREFIX
from functests.test_utils.response_validators import AvgDifficultyResponse


def test_get_avg_difficulty_for_all_songs(cleanup_cache, create_document, cleanup_db):
    create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 8,
        "level": 10,
        "released": "2016-10-26"
    })

    create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 3,
        "level": 9,
        "released": "2016-10-26"
    })

    response = requests.get(URL_PREFIX + '/songs/avg/difficulty')

    assert response.status_code == 200
    avg_diff = AvgDifficultyResponse(**response.json())
    assert (8 + 3) / 2 == avg_diff.average_difficulty
    assert 'all' == avg_diff.level


def test_get_avg_difficulty_for_specific_level(cleanup_cache, create_document, cleanup_db):
    create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 8,
        "level": 10,
        "released": "2016-10-26"
    })

    create_document({
        "artist": "Test artist",
        "title": "test",
        "difficulty": 3,
        "level": 9,
        "released": "2016-10-26"
    })

    create_document({
        "artist": "Test artist2",
        "title": "test",
        "difficulty": 4,
        "level": 9,
        "released": "2016-10-26"
    })

    response = requests.get(URL_PREFIX + '/songs/avg/difficulty?' + urlencode({'level': 9}))

    assert response.status_code == 200
    avg_diff = AvgDifficultyResponse(**response.json())
    assert (7 + 3) / 2 == avg_diff.average_difficulty
    assert 9 == avg_diff.level
