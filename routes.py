# base imports
from datetime import datetime

# Sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse
from sanic.exceptions import NotFound

# Lib import
from lib.exceptions.UserExistsException import UserExistsException
from lib.exceptions.BookingNotFoundException import BookingNotFoundException
from lib.exceptions.UserNotFoundException import UserNotFoundException
from lib.exceptions.ScreenTimeNotFoundException import ScreenTimeNotFoundException
from lib.exceptions.MovieNotFoundException import MovieNotFoundException
from lib.utils.token import checkToken, TOKEN_HEADER

# routes import
from lib.routes.booking import booking_book, booking_pay, booking_internalPayment
from lib.routes.screens import screens_getAll, screens_get, screens_add
from lib.routes.user import user_makeAccount, user_login, user_getBookings, user_logout
from lib.routes.movie import movie_get, movie_add

BYPASS_TOKEN_CHECK = [
    "/api/user/makeAccount",
    "/api/user/login",
    "/api/screens/getAll",
    "/api/screens/get",
    "/api/movies/get"
]

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
    }, status=404)

async def user_exists(request: Request, exception: Exception):
    return json({
        "status": 401,
        "message": f"user {exception.username} already exists. did you forget the password?"
    }, status=401)

async def data_not_found(request: Request, exception: Exception):
    return json({
        "status": 404,
        "message": exception.message
    }, status=400)

# init routes
def add_external_routes(app):
    # GET
    app.add_route(test, '/', methods=["GET"])
    app.add_route(movie_get, "/api/movie/get", methods=["GET"])
    app.add_route(user_getBookings, "/api/user/getBookings", methods=["GET"])
    app.add_route(user_logout, "/api/user/logout", methods=["GET"])
    app.add_route(screens_getAll, "/api/screens/getAll", methods=["GET"])
    app.add_route(screens_get, "/api/screens/get", methods=["GET"])

    # POST
    app.add_route(booking_book, "/api/booking/book", methods=["POST"])
    app.add_route(booking_pay, "/api/booking/pay", methods=["POST"])
    app.add_route(booking_internalPayment, "/api/booking/internalPayment", methods=["POST"])
    app.add_route(movie_add, "/api/movie/add", methods=["POST"])
    app.add_route(screens_add, "/api/screens/add", methods=["POST"])
    app.add_route(user_makeAccount, "/api/user/makeAccount", methods=["POST"])
    app.add_route(user_login, "/api/user/login", methods=["POST"])
    
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
        token_bypass = BYPASS_TOKEN_CHECK.__contains__(request.path)
        if not token_bypass:
            token = request.headers.get(TOKEN_HEADER)
            if token is None:
                return json({
                    "status": 401,
                    "message": "missing token"
                }, status=403)
            if not checkToken(token):
                return json({
                    "status": 403,
                    "message": "invalid token"
                }, status=403)
        pass