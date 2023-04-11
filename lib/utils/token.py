import uuid
from lib.struct.__base import db
from lib.mongo.collection import USER
from lib.struct.user import User

TOKEN_HEADER = "X-Token"

def generateToken() -> str:
    return str(uuid.uuid4())

def checkToken(token: str) -> bool:
    user = db.find(USER, {"tokens": token})
    return not user is None

def getUserByToken(token: str) -> User:
    usr = User().getByToken(token)
    if usr is None:
        return None
    return usr