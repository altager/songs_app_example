__version__ = "0.0.1"
__name__ = "songs_app"

import logging
import os
import ujson as json

from flask import Flask, g
from flask_pymongo import PyMongo
from pymongo import TEXT
from redis import Redis

from songs_app.config import app_config, get_mongo_db_url
from songs_app.dao import SongsDAO, RedisCacheDAO
from songs_app.errors import InvalidQueryParameterError, SongNotFoundError, InvalidRequestParameterError
from songs_app.handlers import SongsHandler
from songs_app.validators.common import ObjectIdURLConverter

logger = logging.getLogger(__name__)


def create_mongo(app, cfg):
    app.config['MONGO_URI'] = get_mongo_db_url(cfg)
    client = PyMongo(app=app)
    g.mongo_db = client.db


def create_redis(cfg):
    g.redis = Redis(host=cfg.REDIS_HOST)


def configure_logger(app):
    logging.basicConfig(format=app.config['LOGGER_FORMAT'], level=app.config['LOGGER_LEVEL'])


def upload_json_data_from_file():
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data/songs.json')
    with open(data_path) as f:
        data = json.load(f)

    # drop previous data and insert new
    g.mongo_db.songs.delete_many({})
    g.mongo_db.songs_rating.delete_many({})
    g.mongo_db.songs.insert_many(data)

    logger.info('Sample data uploaded')


def create_indexes():
    index_names = [i['name'] for i in list(g.mongo_db.songs.list_indexes())]

    if 'level' not in index_names:
        g.mongo_db.songs.create_index('level', background=True, sparse=True, name='level')
    if 'artist_title_text' not in index_names:
        g.mongo_db.songs.create_index([('artist', TEXT), ('title', TEXT)], background=True, name='artist_title_text')


def configure_converters(app):
    app.url_map.converters['object_id'] = ObjectIdURLConverter


def configure_routes(app):
    redis_cache_dao = RedisCacheDAO(redis_connection=g.redis)
    songs_dao = SongsDAO(mongo_connection=g.mongo_db, cache_backend=redis_cache_dao)
    songs_handler = SongsHandler(songs_dao=songs_dao)

    # we should name endpoints explicitly because we use validation decorator
    app.add_url_rule("/songs", endpoint='get_songs_list', view_func=songs_handler.get_songs_list, methods=['GET'])
    app.add_url_rule("/songs/avg/difficulty", endpoint='get_avg_difficulty',
                     view_func=songs_handler.get_avg_difficulty, methods=['GET'])
    app.add_url_rule("/songs/search", endpoint='search_songs', view_func=songs_handler.search_songs, methods=['GET'])
    app.add_url_rule("/songs/rating", endpoint='set_rating', view_func=songs_handler.set_rating, methods=['POST'])
    app.add_url_rule("/songs/avg/rating/<object_id:song_id>", endpoint='get_song_rating',
                     view_func=songs_handler.get_song_rating, methods=['GET'])

    logger.info('Routes created')


def configure_custom_errors(app):
    def handle_error(e): return json.dumps(e.to_dict())

    app.register_error_handler(InvalidQueryParameterError, handle_error)
    app.register_error_handler(InvalidRequestParameterError, handle_error)
    app.register_error_handler(SongNotFoundError, handle_error)


def get_config():
    return app_config[os.getenv('SONGS_APP_CONFIG')] if os.getenv('SONGS_APP_CONFIG') else app_config['default']


def create_app(cfg):
    # create app
    app = Flask(__name__)
    app.config.from_object(cfg)
    # configure logger
    configure_logger(app)
    # configure errors
    configure_custom_errors(app)
    # configure custom url converters
    configure_converters(app)

    with app.app_context():
        # create and store db conn
        create_mongo(app, cfg)
        # create indexes
        create_indexes()
        # create redis for cache
        create_redis(cfg)
        # configure app
        configure_routes(app)
        if cfg.UPLOAD_SAMPLE_DATA:
            # upload existing data from file to db
            upload_json_data_from_file()

    return app
