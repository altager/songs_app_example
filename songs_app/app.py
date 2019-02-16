import argparse
import logging
import os
import ujson as json

from flask import Flask, g
from flask_pymongo import PyMongo
from redis import Redis

from songs_app.config import app_config
from songs_app.db.dao import SongsDAO, RedisCacheDAO
from songs_app.errors import InvalidQueryParameter
from songs_app.handlers import SongsHandler

logger = logging.getLogger(__name__)


def create_mongo(app, cfg):
    app.config['MONGO_URI'] = cfg.MONGO_URL
    client = PyMongo(app=app)
    g.mongo_db = client.db


def create_redis(cfg):
    g.redis = Redis(host=cfg.REDIS_HOST)


def upload_json_data_from_file():
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/songs.json')
    with open(data_path) as f:
        data = json.load(f)

    # drop previous data and insert new
    g.mongo_db.drop_collection('songs')
    g.mongo_db.songs.insert_many(data)


def create_indexes():
    g.mongo_db.songs.create_index('level')


def configure_routes(app):
    redis_cache_dao = RedisCacheDAO(redis_connection=g.redis)
    songs_dao = SongsDAO(mongo_connection=g.mongo_db, cache_backend=redis_cache_dao)
    songs_handler = SongsHandler(songs_dao=songs_dao)

    # we should name endpoints explicitly because of validation 'wrapper' function
    app.add_url_rule("/songs", endpoint='get_songs_list', view_func=songs_handler.get_songs_list, methods=['GET'])
    app.add_url_rule("/songs/avg/difficulty", endpoint='get_avg_difficulty',
                     view_func=songs_handler.get_avg_difficulty, methods=['GET'])
    app.add_url_rule("/songs/search", endpoint='search_songs', view_func=songs_handler.search_songs, methods=['GET'])
    app.add_url_rule("/songs/rating", endpoint='set_rating', view_func=songs_handler.set_rating, methods=['POST'])
    app.add_url_rule("/songs/avg/rating/<int:song_id>", endpoint='get_song_rating',
                     view_func=songs_handler.get_song_rating, methods=['GET'])


def configure_custom_errors(app):
    def handle_error(e): return json.dumps(e.to_dict())

    app.register_error_handler(InvalidQueryParameter, handle_error)


def get_config():
    return app_config[os.getenv('SONGS_APP_CONFIG')] if os.getenv('SONGS_APP_CONFIG') else app_config['default']


def create_app(cfg):
    # create app
    app = Flask(__name__)
    app.config.from_object(cfg)
    # configure errors
    configure_custom_errors(app)

    with app.app_context():
        # create and store db conn
        create_mongo(app, cfg)
        # create redis for cache
        create_redis(cfg)
        # configure app
        configure_routes(app)
        # upload existing data from file to db
        upload_json_data_from_file()

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="songs_app server")
    parser.add_argument('--host')
    parser.add_argument('--port')
    args = parser.parse_args()

    config = get_config()
    os.environ.setdefault('WERKZEUG_DEBUG_PIN', 'off')
    create_app(config).run(host=args.host, port=args.port, debug=config, use_reloader=False)
