# Songs application
Simple API example with Flask, MongoDB, Redis(cache). 

## Install

### With Docker
Execute everything in containers (tests also will be executed in standalone container)

``` 
docker-compose -f docker-compose.yml up -d 
```

### Locally
1. Run dependencies in docker

```
docker-compose -f docker-compose.deps.yml up -d 
```
2. Set up environment variables for app and tests (default or prod)

```
export SONGS_APP_CONFIG=default TEST_CONFIG=default
```
(Optionally) If you want you can override some variables

```
UPLOAD_SAMPLE_DATA=True - upload sample data from songs_app/sample_data/songs.json (default True)
SONGS_APP_DB - full url for mongodb connection. Example: mongodb://user:pass@host:port/db_name?authSource=admin
```
3. Create venv or/and install dependencies from requirements.txt

```
pip install -r requirements.txt
pip install -r ./functests/requirements.txt
```
4. Run application (with python3.*). Run --help if needed

```
python main.py --host localhost --port 8080
```
5. (Optionally) Run tests from ./functests directory

```
pytest
```

## Features
- Request (query, body) validation with attrs.
- Custom json response errors (i.e SongNotFoundError and so on)
- Caching support for 'songs avg difficulty' and 'rating' with Redis
- docker/docker-compose
- Standalone functional (integration) tests with pytest
- MongoDB text indexes for songs searching (better to do with Elastic in future)
- TODO: add pipenv
- TODO: api docs with Swagger
- TODO: typing
- TODO: fix setup file
- TODO: cron tasks for calculation methods (idk if its needed at this time)
- TODO Log into file
- TODO: add sharding etc