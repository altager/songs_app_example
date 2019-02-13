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

    @staticmethod
    def get_db_url():
        return f'mongodb://{DefaultConfig.MONGO_USER}:{DefaultConfig.MONGO_PASS}' \
            f'@{DefaultConfig.MONGO_HOST}:{DefaultConfig.MONGO_PORT}' \
            f'/{DefaultConfig.MONGO_DATABASE_NAME}?authSource=admin'


class DockerDebugConfig(DefaultConfig):
    MONGO_HOST = 'mongo'


app_config = {
    'default': DefaultConfig,
    'docker_debug': DockerDebugConfig,
}
