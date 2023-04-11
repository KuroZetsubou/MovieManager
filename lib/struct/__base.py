# project import
import config
from lib.mongo.connection import MongoConnection

db = MongoConnection(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}", config.MONGO_DB)