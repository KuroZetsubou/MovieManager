# base imports
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime, time

# Sanic import
import sanic
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse
from sanic.exceptions import NotFound
from aiofiles import os as async_os

# Lib import
from lib.mongo.connection import MongoConnection
from lib.omdb_api import OMDbApiWrapper
from lib.exceptions.UserExistsException import UserExistsException
from lib.exceptions.BookingNotFoundException import BookingNotFoundException
from lib.exceptions.UserNotFoundException import UserNotFoundException
from lib.exceptions.ScreenTimeNotFoundException import ScreenTimeNotFoundException
from lib.exceptions.MovieNotFoundException import MovieNotFoundException

# routes import
from lib.routes.user import user_makeAccount

omdb_api = OMDbApiWrapper()

# some first inits
NOT_FOUND = json({
    "error": "FILE_NOT_FOUND",
    "status_code": 404
}, status=404)

async def test(request):
    return json({"message": "hello world."})

async def ignore_404s(request: Request, exception: Exception):
    return json({
        "status": 404,
        "message": f"not found - {request.url}"
    })

async def user_exists(request: Request, exception: Exception):
    return json({
        "status": 401,
        "message": f"user {exception.username} already exists. did you forget the password?"
    })

async def data_not_found(request: Request, exception: Exception):
    return json({
        "status": 404,
        "message": exception.message
    })

# init routes
def add_external_routes(app):
    # GET
    app.add_route(test, '/', methods=["GET"])

    # POST
    app.add_route(user_makeAccount, "/api/user/makeAccount", methods=["POST"])

    # NotFound
    app.error_handler.add(NotFound, ignore_404s)
    app.error_handler.add(UserExistsException, user_exists)
    app.error_handler.add(UserNotFoundException, data_not_found)
    app.error_handler.add(BookingNotFoundException, data_not_found)
    app.error_handler.add(ScreenTimeNotFoundException, data_not_found)
    app.error_handler.add(MovieNotFoundException, data_not_found)

    @app.middleware('response')
    async def print_on_response(request: Request, response: BaseHTTPResponse):
        response.headers['server'] = "MovieManager"
        pass

    @app.middleware('request')
    async def prerequest(request: Request):
        pass