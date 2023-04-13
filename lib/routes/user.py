# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
from lib.struct.__base import db
from lib.struct.user import User, UserType
from lib.struct.booking import Booking
from lib.utils.token import generateToken, getUserByToken, TOKEN_HEADER
from lib.exceptions.UserNotFoundException import UserNotFoundException

# POST: /api/user/makeAccount
async def user_makeAccount(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("username") is None or body.get("password") is None:
        return json({
            "status": 400,
            "message": "invalid request - missing username or password on body"
        }, status=400)
    if body.get("firstName") is None or body.get("lastname") is None:
        return json({
            "status": 400,
            "message": "invalid request - missing firstName and/or lastname on body"
        })
    # compiling struct
    user = User()
    utype = body.get("usertype")
    if utype is None:
        user.usertype = UserType.CLIENT
    else:
        utype = int(utype)
        if utype == 1:
            utype = UserType.ADMIN
        elif utype == 2:
            utype = UserType.EMPLOYEE
        else:
            utype = UserType.CLIENT
        user.usertype = utype 
    user.username = body.get("username")
    user.password = body.get("password")
    user.firstName = body.get("firstName")
    user.lastname = body.get("lastname")
    user.addOnDb()
    # return success
    return json({
        "status": 200,
        "message": f"user {user.username} created"
    })

# POST: /api/user/login
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
    
# GET: /api/user/getBookings
async def user_getBookings(request: Request) -> BaseHTTPResponse:
    user = getUserByToken(request.headers.get(TOKEN_HEADER))
    if user is None:
        raise UserNotFoundException("user not found")
    tempBookings = Booking().getByUserId(user.id)
    bookings = []
    for entry in tempBookings:
        bookings.append(entry.toJson())
    return json({
        "status": 200,
        "bookings": bookings
    })

# GET: /api/user/logout
async def user_logout(request: Request) -> BaseHTTPResponse:
    token = request.headers.get(TOKEN_HEADER)
    user = getUserByToken(token)
    if user is None:
        raise UserNotFoundException("user not found")
    user.logout(token)
    return json({
        "status": 200,
        "message": "ok"
    })