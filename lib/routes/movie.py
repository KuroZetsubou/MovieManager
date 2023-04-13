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

# GET: /api/movie/getAll
async def movie_getAll(request: Request) -> BaseHTTPResponse:
    temp = Movie().getAll()
    movies = []
    for entry in temp:
        movies.append(entry.toJson())
    return json({
        "status": 200,
        "screens": movies
    })

# GET: /api/movie/get
async def movie_get(request: Request) -> BaseHTTPResponse:
    body = request.args

    if body.get("movieId") is None:
        return json({
            "status": 400,
            "message": "missing movieId value"
        }, status=400)
    
    movie = Movie().getById(body.get("movieId"))

    movieDetails = omdb_api.searchTitle(movie.omdbName)
    
    return json({
        "status": 200,
        "movie": movie.toJson(),
        "movieDetails": movieDetails
    })

# POST: /api/movie/add
async def movie_add(request: Request) -> BaseHTTPResponse:
    body = request.json
    # check if user is client. if so, kick out
    usr = User().getByToken(request.headers.get(TOKEN_HEADER))
    if usr.usertype == UserType.CLIENT:
        return json({
            "status": 403,
            "message": "forbidden"
        }, status=403)
    # input data check
    if body.get("movieName") is None:
        return json({
            "status": 400,
            "message": "missing movieName value"
        }, status=400)
    # omdbName check
    omdbName = body.get("omdbName")
    omdbName = omdbName if not omdbName is None else body.get("movieName")
    # insert data on database
    movie = Movie()
    movie.omdbName = omdbName
    movie.movieName = body.get("movieName")
    _id = movie.addOnDb()
    return json({
        "status": 200,
        "message": "ok.",
        "id": _id
    })