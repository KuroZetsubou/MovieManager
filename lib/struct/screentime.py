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

    def getById(self, id: str) -> ScreenTime:
        data = db.find(SCREENTIME, {"_id": id})
        if data is None:
            raise ScreenTimeNotFoundException(f"user id {id} not found")
        return self.__compileDataFromMongo(data)
    
    def __compileDataFromMongo(self, mongoResult: object) -> ScreenTime:
        self.screenTime = mongoResult["screenTime"]
        self.capacity = mongoResult["capacity"]
        self.movie = Movie()
        self.movie = self.movie.getById(mongoResult["movie"])
        self.id = mongoResult["_id"]
        return self
    
    # add this instance on database
    def addOnDb(self, id : int):
        db.insert(SCREENTIME, {
            "_id": id,
            "screenTime": self.screenTime,
            "capacity": self.capacity,
            "movie": self.movie.id,
        })