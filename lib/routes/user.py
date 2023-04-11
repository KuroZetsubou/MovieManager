# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
import config
from lib.mongo.connection import MongoConnection

db = MongoConnection(f"mongodb://{config.MONGO_HOST}:{config.MONGO_PORT}", config.MONGO_DB)

# POST: /api/user/makeAccount
async def user_makeAccount(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("username") is None or body.get("password") is None:
        return json({
            "status": 400,
            "message": "invalid request - missing username or password on body"
        })
    print(db)
    return json({
        "status": 200,
        "message": "db is connected and reachable"
    })