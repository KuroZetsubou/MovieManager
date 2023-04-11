# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
from lib.struct.__base import db, omdb_api
from lib.struct.user import User, UserType
from lib.struct.booking import Booking
from lib.struct.screentime import ScreenTime
from lib.utils.token import generateToken, getUserByToken, TOKEN_HEADER
from lib.exceptions.UserNotFoundException import UserNotFoundException

# GET: /api/screens/getAll
async def screens_getAll(request: Request) -> BaseHTTPResponse:
    temp = ScreenTime().getAll()
    screens = []
    for entry in temp:
        screens.append(entry.toJson())
    return json({
        "status": 200,
        "screens": screens
    })

# GET: /api/screens/get
async def screens_get(request: Request) -> BaseHTTPResponse:
    body = request.args

    if body.get("screenId") is None:
        return json({
            "status": 400,
            "message": "missing screenId value"
        }, status=400)
    
    screen = ScreenTime().getById(body.get("screenId"))
    bookings = Booking().getByScreenTime(screen)
    movie = screen.movie
    takenSlots = []

    movieDetails = omdb_api.searchTitle(movie.omdbName)

    for booking in bookings:
        for slot in booking.slots:
            takenSlots.append(slot)
    
    return json({
        "status": 200,
        "screen": screen.toJson(),
        "takenSlots": takenSlots,
        "movieDetails": movieDetails
    })