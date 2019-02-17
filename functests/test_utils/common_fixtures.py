import os

import pymongo
import pytest
from redis import Redis

from functests.config import app_config, get_mongo_db_url

__all__ = [
    'cfg',
    'db',
    'cleanup_db',
    'redis',
    'cleanup_cache'
]


@pytest.fixture(scope='session')
def cfg():
    return app_config[os.getenv('TEST_CONFIG')] if os.getenv('TEST_CONFIG') else app_config['default']


@pytest.fixture(scope='session')
def db(cfg):
    client = pymongo.MongoClient(get_mongo_db_url(cfg))
    return client.songs_db


@pytest.fixture
def cleanup_db(db):
    db.songs.delete_many({})


@pytest.fixture(scope='session')
def redis(cfg):
    return Redis(host=cfg.REDIS_HOST)


@pytest.fixture()
def cleanup_cache(redis):
    # TODO: replace in future
    redis.flushall()
