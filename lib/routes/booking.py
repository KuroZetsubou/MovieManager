# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
from lib.struct.__base import db
from lib.struct.user import User, UserType
from lib.struct.booking import Booking
from lib.struct.screentime import ScreenTime
from lib.struct.screentime import Movie
from lib.utils.token import generateToken, getUserByToken, TOKEN_HEADER
from lib.exceptions.UserNotFoundException import UserNotFoundException

# POST: /api/booking/book
async def booking_book(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("movieId") is None:
        return json({
            "status": 400,
            "message": "missing movieId value"
        }, status=400)
    if body.get("screenId") is None:
        return json({
            "status": 400,
            "message": "missing screenId value"
        }, status=400)
    slots = body.get("slots")
    usr = User().getByToken(request.headers.get(TOKEN_HEADER))
    booking = Booking()
    booking.movie = Movie().getById(body.get("movieId"))
    booking.user = usr
    booking.screenTime = ScreenTime().getById(body.get("screenId"))
    booking.slots = [] if slots is None else slots
    booking.addOnDb()
    return json({
        "status": 200,
        "message": "ok"
    })

# POST: /api/booking/pay
async def booking_pay(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("bookingId") is None:
        return json({
            "status": 400,
            "message": "missing bookingId"
        }, status=400)
    usr = User().getByToken(request.headers.get(TOKEN_HEADER))
    if usr.usertype != UserType.CLIENT:
        return json({
            "status": 403,
            "message": "endpoint reserved for clients paying. for employee use /api/booking/internalPayment"
        }, status=403)
    booking = Booking().getById(body.get("bookingId"))
    booking.pay()
    return json({
        "status": 200,
        "message": "ok"
    })

# POST: /api/booking/internalPayment
async def booking_internalPayment(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("bookingId") is None:
        return json({
            "status": 400,
            "message": "missing bookingId"
        }, status=400)
    usr = User().getByToken(request.headers.get(TOKEN_HEADER))
    if usr.usertype != UserType.EMPLOYEE and usr.usertype != UserType.ADMIN:
        return json({
            "status": 403,
            "message": "endpoint reserved for clients paying. for clients use /api/booking/pay"
        }, status=403)
    booking = Booking().getById(body.get("bookingId"))
    booking.pay()
    return json({
        "status": 200,
        "message": "ok"
    })