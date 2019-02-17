import argparse
import os

from songs_app import create_app, get_config

app = create_app(get_config())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="songs_app server")
    parser.add_argument("--host")
    parser.add_argument("--port")
    args = parser.parse_args()

    config = get_config()
    os.environ.setdefault("WERKZEUG_DEBUG_PIN", "off")
    app.run(host=args.host, port=args.port, debug=config.DEBUG, use_reloader=False)
