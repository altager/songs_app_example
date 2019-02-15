#!/usr/bin/env bash
set -e

./bin/wait-for-it.sh mongo:27017 -t 25

if [[ $1 = 'app' ]]; then
    python -m songs_app.main --host 0.0.0.0 --port 8080
fi

if [[ $1 = 'tests' ]]; then
    pytest --spec -p no:cacheprovider --tb short -vv .
fi

if [[ $1 = 'sleep' ]]; then
    sleep infinity
fi

exec "$@"
