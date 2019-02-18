#!/usr/bin/env bash
set -e

./bin/wait-for-it.sh mongo:27017 -t 25
./bin/wait-for-it.sh redis:6379 -t 25

if [[ $1 = 'app' ]]; then
    gunicorn --bind 0.0.0.0:8080 --workers=2 --log-level=info songs_app.main:app
fi

if [[ $1 = 'tests' ]]; then
    ./bin/wait-for-it.sh songs_app:8080 -t 25
    find -name "*.pyc" -delete
    pytest --spec -p no:cacheprovider --tb short -vv .
fi

if [[ $1 = 'sleep' ]]; then
    sleep infinity
fi

exec "$@"
