import argparse
import logging
import os

import ujson as json
from flask import Flask, g
from flask_pymongo import PyMongo

from songs_app.config import app_config
from songs_app.db.dao import SongsDAO
from songs_app.handlers import SongsHandler

logger = logging.getLogger(__name__)


def create_mongo(app, cfg):
    app.config['MONGO_URI'] = os.environ.get('SONGS_APP_DB') if os.environ.get('SONGS_APP_DB') else cfg.get_db_url()
    client = PyMongo(app=app)
    g.mongo_db = client.db


def upload_json_data_from_file():
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/songs.json')
    with open(data_path) as f:
        data = json.load(f)

    # drop previous data and insert new
    g.mongo_db.drop_collection('songs')
    g.mongo_db.songs.insert_many(data)


def configure_routes(app):
    songs_dao = SongsDAO(mongo_connection=g.mongo_db)
    songs_handler = SongsHandler(songs_dao=songs_dao)

    app.add_url_rule("/songs", view_func=songs_handler.get_songs, methods=['GET'])
    app.add_url_rule("/songs/avg/difficulty", view_func=songs_handler.get_difficulty, methods=['GET'])
    app.add_url_rule("/songs/search", view_func=songs_handler.search_songs, methods=['GET'])
    app.add_url_rule("/songs/rating", view_func=songs_handler.set_rating, methods=['POST'])
    app.add_url_rule("/songs/avg/rating/<int:song_id>", view_func=songs_handler.get_difficulty, methods=['GET'])


def create_app(cfg):
    # create app
    app = Flask(__name__)
    app.config.from_object(cfg)

    # create and store db conn in app context
    with app.app_context():
        create_mongo(app, cfg)
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

    config = app_config[os.getenv('SONGS_APP_CONFIG')] if os.getenv('SONGS_APP_CONFIG') else app_config['default']
    os.environ.setdefault('WERKZEUG_DEBUG_PIN', 'off')
    create_app(cfg=config).run(host=args.host, port=args.port, debug=config, use_reloader=False)
