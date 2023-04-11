import uuid
from lib.struct.__base import db
from lib.mongo.collection import USER

def generateToken() -> str:
    return str(uuid.uuid4())

def checkToken(token: str) -> bool:
    user = db.find(USER, {"tokens": token})
    return not user is None