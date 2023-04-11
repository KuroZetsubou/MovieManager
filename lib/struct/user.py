from hashlib import sha256
from enum import Enum

# project import
import config
from lib.mongo.connection import MongoConnection
from lib.mongo.collection import USER
from lib.exceptions.UserNotFoundException import UserNotFoundException

db = MongoConnection(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}", config.MONGO_DB)

class UserType(Enum):
    ADMIN = 1
    EMPLOYEE = 2
    CLIENT = 3

class User:
    
    def __init__(self, 
                 username: str | None = None, 
                 password: str | None = None,
                 usertype: UserType = UserType.CLIENT,
                 firstName: str | None = None,
                 lastname: str | None = None,
                 tokens: list = []):
        self.username = username
        self.password = password
        self.usertype = usertype
        self.firstName = firstName
        self.lastname = lastname
        self.tokens = tokens
        self.id = None
        pass

    def getById(self, id: str) -> User:
        data = db.find(USER, {"_id": id})
        if data is None:
            raise UserNotFoundException(f"user id {id} not found")
        return self.__compileDataFromMongo(data)

    def getByUsername(self, username: str) -> User:
        data = db.find(USER, {"username": username})
        if data is None:
            raise UserNotFoundException(f"username {username} not found")
        return self.__compileDataFromMongo(data)

    def __compileDataFromMongo(self, mongoResult: object) -> User:
        self.username = mongoResult["username"]
        self.password = mongoResult["password"]
        self.usertype = mongoResult["usertype"]
        self.firstName = mongoResult["firstName"]
        self.lastname = mongoResult["lastname"]
        self.tokens = mongoResult["tokens"]
        self.id = mongoResult["_id"]
        return self

    # add this instance on database
    def addOnDb(self):
        db.insert(USER, {
            "_id": sha256(self.username).hexdigest(),
            "username": self.username,
            "password": self.__securePassword(self.password),
            "usertype": self.usertype,
            "firstName": self.firstName,
            "tokens": self.tokens,
        })

    # TODO
    # can be used also for verification
    def __securePassword(self, password: str) -> str:
        return password
    
    def checkPasswordFromPlaintext(self, plaintextPassword: str) -> bool:
        return self.__securePassword(plaintextPassword) == self.password
