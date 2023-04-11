# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
from lib.struct.__base import db
from lib.struct.user import User, UserType
from lib.utils.token import generateToken

# POST: /api/user/makeAccount
async def user_makeAccount(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("username") is None or body.get("password") is None:
        return json({
            "status": 400,
            "message": "invalid request - missing username or password on body"
        }, status=400)
    # compiling struct
    user = User()
    user.username = body.get("username")
    user.password = body.get("password")
    user.usertype = UserType.CLIENT
    user.firstName = body.get("firstName")
    user.lastname = body.get("lastname")
    user.addOnDb()
    # return success
    return json({
        "status": 200,
        "message": f"user {user.username} created"
    })

async def user_login(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("username") is None or body.get("password") is None:
        return json({
            "status": 400,
            "message": "invalid request - missing username or password on body"
        })
    user = User().getByUsername(body.get("username"))
    isOk = user.checkPasswordFromPlaintext(body.get("password"))
    if isOk:
        token = generateToken()
        user.addToken(token=token)
        return json({
            "status": 200,
            "message": "ok",
            "token": token
        })
    else:
        return json({
            "status": 401,
            "message": "invalid credentials"
        }, status=401)