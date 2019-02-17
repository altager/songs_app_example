# Songs application
Simple API example with Flask, MongoDB, Redis. 

## Install

## Features
- Request (query, body) validation with attrs.
- Custom json response errors (i.e SongNotFoundError and so on)
- Caching for 'songs avg difficulty' and 'rating' with Redis
- Docker deployment
- Standalone functional (integration) tests with pytest
- MongoDB text indexes for songs searching (better to do with Elastic in future)
- TODO: api docs with Swagger
- TODO: Gunicorn app execution
- TODO: typing
- TODO: cron tasks for calculation methods
- TODO: DISABLE DEBUG MODE!

## Project structure overview
./app.py -> main app file. entrypoint
./db/dao