# MovieManager
Backend side for Movie booking for a cinema

## Requirements

* Python 3.10 or newer
* MongoDB 3.2+ (using docker or local installation, both are fine)

## Installation

* Install all possible dependencies with `python3 -m pip install -r requirements.txt`
* Make sure that MongoDB database is loaded and reachable from your host
* Run `python3 bootstrap.py`, it will preload some initial data for movies and screenings
* Run `python3 main.py` for loading the server application
* Enjoy

## Config

Opening the `config.py`:

```python
# OMDB API Key (get from http://www.omdbapi.com/apikey.aspx)
API_KEY_OMDB = "" # Add token here

# MongoDB wrapper
MONGO_HOST = "0.0.0.0"
MONGO_PORT = 27017
MONGO_USER = None
MONGO_PASS = None
MONGO_DB   = "MovieManager"

# Server Settings
SANIC_HOST  = "0.0.0.0"
SANIC_PORT  = 80
SANIC_DEBUG = False

# Application settings
BOOKING_MAX_TIME_BEFORE = 3600 # amount of seconds before the screen time. gap allowed for clients before having it unavailable. it's bypassed only by employees (for local purchase of tickets)
```

## Testing environment

### Requirements

* Insomnia

### How to prepare

* Open `Insomnia`
* Click on the `Preferences` on the bottom-left side of the window (with the gear icon)
* Go on `Data` tab
* Click on `Import Data` -> `From File` (pick the file stored at `docs/insomnia_envi.json`)
* Restored the environment, you can try to test the API