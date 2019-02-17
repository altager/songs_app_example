import os


class DefaultTestConfig:
    MONGO_USER = "songs_user"
    MONGO_PASS = "songs_pass"
    MONGO_HOST = "localhost"
    MONGO_PORT = "27017"
    MONGO_DATABASE_NAME = "songs_db"
    REDIS_HOST = "localhost"
    URL_PREFIX = "http://localhost:5000"


class DockerTestConfig(DefaultTestConfig):
    MONGO_HOST = "mongo"
    REDIS_HOST = "redis"
    URL_PREFIX = "http://songs_app:8080"


def get_mongo_db_url(cfg):
    return (
        os.environ.get("SONGS_APP_DB")
        or f"mongodb://{cfg.MONGO_USER}:{cfg.MONGO_PASS}@{cfg.MONGO_HOST}:"
        f"{cfg.MONGO_PORT}/{cfg.MONGO_DATABASE_NAME}?authSource=admin"
    )


app_config = {"default": DefaultTestConfig, "docker": DockerTestConfig}
