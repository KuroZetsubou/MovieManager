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

    def getById(self, id: int) -> Movie:
        data = db.find(MOVIE, {"_id": id})
        if data is None:
            raise MovieNotFoundException(f"movie id {id} not found")
        return self.__compileDataFromMongo(data)
    
    def getByMovieName(self, movieName: str) -> Movie:
        data = db.find(MOVIE, {"movieName": movieName})
        if data is None:
            raise MovieNotFoundException(f"movie {movieName} not found")
        return self.__compileDataFromMongo(data)
    
    def __compileDataFromMongo(self, mongoResult: object) -> Movie:
        self.movieName = mongoResult["movieName"]
        self.omdbName = mongoResult["omdbName"]
        self.id = mongoResult["_id"]
        return self

    def addOnDb(self, id: int):
        db.insert(MOVIE, {
            "_id": id,
            "movieName": self.movieName,
            "omdbName": self.omdbName
        })
    
