from hashlib import sha256
from enum import IntEnum
from pymongo.errors import DuplicateKeyError

# project import
import config
from lib.mongo.connection import MongoConnection
from lib.mongo.collection import USER
from lib.exceptions.UserNotFoundException import UserNotFoundException
from lib.exceptions.UserExistsException import UserExistsException

db = MongoConnection(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}", config.MONGO_DB)

class UserType(IntEnum):
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

    def getById(self, id: str):
        data = db.find(USER, {"_id": id})
        if data is None:
            raise UserNotFoundException(f"user id {id} not found")
        return self.__compileDataFromMongo(data)

    def getByUsername(self, username: str):
        data = db.find(USER, {"username": username})
        if data is None:
            raise UserNotFoundException(f"username {username} not found")
        return self.__compileDataFromMongo(data)

    def getByToken(self, token: str):
        usr = db.find(USER, {"tokens": token})
        if usr is None:
            return None
        return self.__compileDataFromMongo(usr)

    def __compileDataFromMongo(self, mongoResult: object):
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
        try:
            _id = sha256(self.username.encode("utf8")).hexdigest()
            db.insert(USER, {
                "_id": _id,
                "username": self.username,
                "password": self.__securePassword(self.password),
                "usertype": self.usertype,
                "firstName": self.firstName,
                "lastname": self.lastname,
                "tokens": self.tokens,
            })
            return _id
        except DuplicateKeyError:
            raise UserExistsException(username=self.username)

    # can be used also for verification
    def __securePassword(self, password: str) -> str:
        return sha256(f"{self.username}-{password}".encode("utf-8")).hexdigest()
    
    def checkPasswordFromPlaintext(self, plaintextPassword: str) -> bool:
        return self.__securePassword(plaintextPassword) == self.password

    def addToken(self, token: str):
        if self.id is None:
            raise Exception("user is not defined from mongo.")
        self.tokens.append(token)
        self.__setToken()
        pass

    def logout(self, token: str):
        self.tokens.remove(token)
        self.__setToken()

    def revokeTokens(self):
        self.tokens = []
        self.__setToken()

    def __setToken(self):
        db.updateOne(USER, {"_id": self.id}, {"$set": {"tokens": self.tokens}})
        
    def toJson(self):
        return {
            "username": self.username,
            "usertype": self.usertype,
            "firstName": self.firstName,
            "lastname": self.lastname
        }