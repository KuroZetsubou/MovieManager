# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
from lib.struct.__base import db
from lib.struct.user import User, UserType
from lib.struct.booking import Booking
from lib.struct.screentime import ScreenTime
from lib.utils.token import generateToken, getUserByToken, TOKEN_HEADER
from lib.exceptions.UserNotFoundException import UserNotFoundException

# GET: /api/screens/getAll
async def screens_getAll(request: Request) -> BaseHTTPResponse:
    screens = ScreenTime().getAll()
    return json({
        "status": 200,
        "screens": screens
    })