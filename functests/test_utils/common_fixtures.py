import pymongo
import pytest
from redis import Redis

from functests.config import DefaultTestConfig

__all__ = [
    'db',
    'cleanup_db',
    'redis',
    'cleanup_cache'
]


@pytest.fixture(scope='session')
def db():
    client = pymongo.MongoClient(DefaultTestConfig.MONGO_URL)
    return client.songs_db


@pytest.fixture
def cleanup_db(db):
    db.drop_collection('songs')


@pytest.fixture(scope='session')
def redis():
    return Redis(host=DefaultTestConfig.REDIS_HOST)


@pytest.fixture()
def cleanup_cache(redis):
    # TODO: replace in future
    redis.flushall()
