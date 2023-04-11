from time import time
# project import
from lib.mongo.collection import SCREENTIME
from lib.exceptions.ScreenTimeNotFoundException import ScreenTimeNotFoundException
from lib.struct.movie import Movie
from lib.struct.__base import db

class ScreenTime:

    def __init__(self,
                 movie: Movie | None = None,
                 screenTime: int | None = None,
                 capacity: int = 300
                 ) -> None:
        self.movie = movie
        self.screenTime = screenTime
        self.capacity = capacity
        pass

    def getById(self, id: str):
        data = db.find(SCREENTIME, {"_id": id})
        if data is None:
            raise ScreenTimeNotFoundException(f"user id {id} not found")
        return self.__compileDataFromMongo(data)
    
    # gets all upcoming screens
    def getAll(self):
        data = db.findMany(SCREENTIME, {"screenTime": {"$gt": int(time())}})
        return self.__compileListFromMongo(data)
    
    def __compileDataFromMongo(self, mongoResult: object):
        self.screenTime = mongoResult["screenTime"]
        self.capacity = mongoResult["capacity"]
        self.movie = Movie()
        self.movie = self.movie.getById(mongoResult["movie"])
        self.id = mongoResult["_id"]
        return self
    
    def __compileDataFromMongoAsExternal(self, mongoResult: object):
        obj = ScreenTime()
        return obj.__compileDataFromMongo(mongoResult)
    
    def __compileListFromMongo(self, mongoList: list) -> list:
        data = []
        for entry in mongoList:
            data.append(self.__compileDataFromMongoAsExternal(entry))
        return data
    
    # add this instance on database
    def addOnDb(self, id : int):
        db.insert(SCREENTIME, {
            "_id": id,
            "screenTime": self.screenTime,
            "capacity": self.capacity,
            "movie": self.movie.id,
        })