from urllib.parse import urlencode

import pytest
import requests

from functests.test_utils.response_validators import AvgDifficultyResponse, ErrorResponse


def test_get_avg_difficulty_for_all_songs(cleanup_cache, create_document, cleanup_db, cfg):
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

    response = requests.get(cfg.URL_PREFIX + '/songs/avg/difficulty')

    assert response.status_code == 200
    avg_diff = AvgDifficultyResponse(**response.json())
    assert (8 + 3) / 2 == avg_diff.average_difficulty
    assert 'all' == avg_diff.level


def test_get_avg_difficulty_for_specific_level(cleanup_cache, create_document, cleanup_db, cfg):
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

    response = requests.get(cfg.URL_PREFIX + '/songs/avg/difficulty?' + urlencode({'level': 9}))

    assert response.status_code == 200
    avg_diff = AvgDifficultyResponse(**response.json())
    assert (4 + 3) / 2 == avg_diff.average_difficulty
    assert 9 == avg_diff.level


def test_get_avg_difficulty_not_existing_level(cfg):
    response = requests.get(cfg.URL_PREFIX + '/songs/avg/difficulty?' + urlencode({'level': 999}))

    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.parametrize('level', [-1, 'a', 1.01])
def test_get_avg_difficulty_invalid_level(level, cfg):
    response = requests.get(cfg.URL_PREFIX + '/songs/avg/difficulty?' + urlencode({'level': level}))

    assert response.status_code == 400
    error = ErrorResponse(**response.json())
    assert error.message == 'invalid_query_parameter'
