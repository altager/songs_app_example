import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_secret_key() -> str:
    secret_file = os.path.join(basedir, '../.secret')
    if not os.path.isfile(secret_file):
        sec_key = os.urandom(24)
        with open(secret_file, 'w') as f:
            f.write(str(sec_key))
        gitignore_file = os.path.join(basedir, '../.gitignore')
        with open(gitignore_file, 'a+') as f:
            if '.secret' not in f.readlines() and '.secret\n' not in f.readlines():
                f.write('.secret\n')
    # Read SECRET_KEY from .secret file
    with open(secret_file, 'r') as f:
        sec_key = f.read().strip()

    return sec_key


class DefaultConfig:
    SECRET_KEY = get_secret_key()
    DEBUG = True
    MONGO_USER = 'songs_user'
    MONGO_PASS = 'songs_pass'
    MONGO_HOST = 'localhost'
    MONGO_PORT = '27017'
    MONGO_DATABASE_NAME = 'songs_db'
    REDIS_HOST = 'localhost'
    UPLOAD_SAMPLE_DATA = os.environ.get('UPLOAD_SAMPLE_DATA') or True
    LOGGER_FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s]  %(message)s'
    LOGGER_LEVEL = 10  # CRITICAL=50, ERROR=40, WARNING=30, INFO=20, DEBUG=10, NOTSET=0
    CACHE_TTL_DIFFICULTY = 60
    CACHE_TTL_RATING = 60


class DockerDebugConfig(DefaultConfig):
    MONGO_HOST = 'mongo'
    REDIS_HOST = 'redis'
    LOGGER_LEVEL = 10


def get_mongo_db_url(cfg):
    return os.environ.get('SONGS_APP_DB') or \
           f'mongodb://{cfg.MONGO_USER}:{cfg.MONGO_PASS}@{cfg.MONGO_HOST}:' \
               f'{cfg.MONGO_PORT}/{cfg.MONGO_DATABASE_NAME}?authSource=admin'


class DockerProdConfig(DockerDebugConfig):
    # How it could be in real
    DEBUG = False
    LOGGER_LEVEL = 40


app_config = {
    'default': DefaultConfig,
    'docker_debug': DockerDebugConfig,
    'docker_prod': DockerProdConfig
}
