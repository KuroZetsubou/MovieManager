# OMDB API Key (get from http://www.omdbapi.com/apikey.aspx)
API_KEY_OMDB = ""

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
SCREENS_DEFAULT_CAPACITY = 300