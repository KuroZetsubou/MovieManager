from hashlib import sha256
from enum import Enum

# project import
import config
from lib.mongo.connection import MongoConnection
from lib.mongo.collection import MOVIE
from lib.exceptions.MovieNotFoundException import MovieNotFoundException

db = MongoConnection(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}", config.MONGO_DB)

class Movie:

    def __init__(self,
                 movieName: str | None = None,
                 omdbName: str | None = None):
        self.movieName = movieName
        self.omdbName = omdbName
        self.id = None
        pass

    def getById(self, id: int):
        data = db.find(MOVIE, {"_id": id})
        if data is None:
            raise MovieNotFoundException(f"movie id {id} not found")
        return self.__compileDataFromMongo(data)
    
    def getByMovieName(self, movieName: str):
        data = db.find(MOVIE, {"movieName": movieName})
        if data is None:
            raise MovieNotFoundException(f"movie {movieName} not found")
        return self.__compileDataFromMongo(data)
    
    def getRandom(self):
        data = db.random(MOVIE)
        return self.__compileDataFromMongo(data)
    
    def __compileDataFromMongo(self, mongoResult: object):
        self.movieName = mongoResult["movieName"]
        self.omdbName = mongoResult["omdbName"]
        self.id = mongoResult["_id"]
        return self

    def addOnDb(self):
        db.insert(MOVIE, {
            "_id": sha256(f"{self.movieName}-{self.omdbName}".encode("utf8")).hexdigest(),
            "movieName": self.movieName,
            "omdbName": self.omdbName
        })
    
    def toJson(self):
        return {
            "movieName": self.movieName,
            "omdbName": self.omdbName
        }
