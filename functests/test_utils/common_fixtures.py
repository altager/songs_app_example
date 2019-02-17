import os

import pymongo
import pytest
from redis import Redis

from functests.config import app_config

__all__ = [
    'config',
    'db',
    'cleanup_db',
    'redis',
    'cleanup_cache'
]


@pytest.fixture(scope='session')
def config():
    return app_config[os.getenv('SONGS_APP_CONFIG')] if os.getenv('SONGS_APP_CONFIG') else app_config['default']


@pytest.fixture(scope='session')
def db(config):
    client = pymongo.MongoClient(config.MONGO_URL)
    return client.songs_db


@pytest.fixture
def cleanup_db(db):
    db.songs.delete_many({})


@pytest.fixture(scope='session')
def redis(config):
    return Redis(host=config.REDIS_HOST)


@pytest.fixture()
def cleanup_cache(redis):
    # TODO: replace in future
    redis.flushall()
