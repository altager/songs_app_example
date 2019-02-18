# Songs application
Simple API example with Flask, MongoDB, Redis(cache). 

GET /songs
  - Returns a list of songs with some details on them
  - Default limit is 5, max limit is 100
  - Use parameter last_id to skip everything before last_id (including last_id)
  
 Examples: 
   - /songs
   - /songs?limit=1
   - /songs?last_id=507f191e810c19729de860ea&limit=2

GET /songs/avg/difficulty
  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.
  
  Examples:
    - /songs/avg/difficulty
    - /songs/avg/difficulty?level=9

GET /songs/search
  - Takes in parameter a 'message' string to search
  - Return a list of songs.
  - Search by title and artist
  - Search is case insensitive
  
  Examples:
    - /songs/search?message=Mr%20Fas

POST /songs/rating
  - Takes in parameter a "song_id" and a "rating"
  - This call adds a rating to the song. Ratings should be between 1 and 5
  
  Examples:
    - {"song_id": "507f191e810c19729de860ea", "rating": 1}
     

GET /songs/avg/rating/<song_id>
  - Returns the average, the lowest and the highest rating of the given song id.
  
  Examples:
    - /songs/avg/rating/507f191e810c19729de860ea

## Install

### With Docker
Execute everything in containers (tests also will be executed in standalone container)

``` 
docker-compose -f docker-compose.yml up -d 
```

### Locally
1. Run dependencies (Mongo, Redis, Mongo express) in docker

```
docker-compose -f docker-compose.deps.yml up -d 
```
2. Set up environment variables for app and tests (default or prod)

```
export SONGS_APP_CONFIG=default TEST_CONFIG=default
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