import config

# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
from lib.struct.__base import db, omdb_api
from lib.struct.user import User, UserType
from lib.struct.booking import Booking
from lib.struct.movie import Movie
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

# POST: /api/screens/add
async def screens_add(request: Request) -> BaseHTTPResponse:
    body = request.json
    # check if user is client. if so, kick out
    usr = User().getByToken(request.headers.get(TOKEN_HEADER))
    if usr.usertype == UserType.CLIENT:
        return json({
            "status": 403,
            "message": "forbidden"
        }, status=403)
    # input data check
    if body.get("movieId") is None:
        return json({
            "status": 400,
            "message": "missing movieId value"
        }, status=400)
    if body.get("screenTime") is None:
        return json({
            "status": 400,
            "message": "missing epoch screentime value"
        }, status=400)
    # capacity check
    capacity = body.get("capacity")
    capacity = capacity if not capacity is None else config.SCREENS_DEFAULT_CAPACITY
    # insert data on database
    screen = ScreenTime()
    screen.movie = Movie().getById(body.get("movieId"))
    screen.capacity = capacity
    screen.screenTime = body.get("screenTime")
    _id = screen.addOnDb()
    return json({
        "status": 200,
        "message": "ok.",
        "id": _id
    })