from enum import Enum

# project import
from lib.mongo.collection import BOOKING
from lib.exceptions.BookingNotFoundException import BookingNotFoundException
from lib.struct.__base import db
from lib.struct.user import User
from lib.struct.movie import Movie
from lib.struct.screentime import ScreenTime

class Booking:

    def __init__(self,
                 user: User | None = None,
                 movie: Movie | None = None,
                 screenTime: ScreenTime | None = None,
                 paid: bool = False,
                 slots: list = []):
        self.user = user
        self.movie = movie
        self.screenTime = screenTime
        self.paid = paid
        self.slots = slots
        self.id = None
        pass

    def getById(self, id: int):
        data = db.find(BOOKING, {"_id": id})
        if data is None:
            raise BookingNotFoundException(f"booking id {id} not found")
        return self.__compileDataFromMongo(data)
    
    def getByMovie(self, movie: Movie) -> list:
        data = db.findMany(BOOKING, {"movie": movie.id})
        if data.__len__() == 0:
            raise BookingNotFoundException(f"booking for movie {movie.movieName} not found")
        return self.__compileDataFromMongo(data)
    
    def getByScreenTime(self, screenTime: ScreenTime) -> list:
        data = db.findMany(BOOKING, {"screenTime": screenTime.id})
        if data.__len__() == 0:
            raise BookingNotFoundException(f"booking for movie {screenTime.id} not found")
        return self.__compileListFromMongo(data)
    
    def getByUserId(self, id: int) -> list:
        data = db.findMany(BOOKING, {"user": id})
        return self.__compileListFromMongo(data)
    
    def __compileDataFromMongo(self, mongoResult: object):
        self.paid = mongoResult["paid"]
        self.slots = mongoResult["slots"]
        self.id = mongoResult["_id"]
        self.user = User().getById(mongoResult["user"])
        self.movie = Movie().getById(mongoResult["movie"])
        self.screenTime = ScreenTime().getById(mongoResult["screenTime"])
        return self
    
    def __compileDataFromMongoAsExternal(self, mongoResult: object):
        booking = Booking()
        return booking.__compileDataFromMongo(mongoResult)
    
    def __compileListFromMongo(self, mongoList: list) -> list:
        data = []
        for entry in mongoList:
            data.append(self.__compileDataFromMongoAsExternal(entry))
        return data

    def addOnDb(self, id: int):
        db.insert(BOOKING, {
            "_id": id,
            "paid": self.paid,
            "slots": self.slots,
            "user": self.user.id,
            "movie": self.movie.id,
            "screenTime": self.screenTime.id
        })
    