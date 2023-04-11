# project import
import config
from lib.mongo.connection import MongoConnection
from lib.omdb_api import OMDbApiWrapper

db = MongoConnection(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}", config.MONGO_DB)
omdb_api = OMDbApiWrapper()