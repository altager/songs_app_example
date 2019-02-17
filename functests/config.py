import os


class DefaultTestConfig:
    MONGO_USER = 'songs_user'
    MONGO_PASS = 'songs_pass'
    MONGO_HOST = 'localhost'
    MONGO_PORT = '27017'
    MONGO_DATABASE_NAME = 'songs_db'
    MONGO_URL = os.environ.get('SONGS_APP_DB') or \
                f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE_NAME}?authSource=admin'
    REDIS_HOST = 'localhost'
    REDIS_URL = os.environ.get('REDIS_URL') or f'redis://{REDIS_HOST}:6379/'


class DockerTestConfig(DefaultTestConfig):
    MONGO_HOST = 'mongo'
    REDIS_HOST = 'redis'


app_config = {
    'default': DefaultTestConfig,
    'docker_debug': DockerTestConfig,
}
