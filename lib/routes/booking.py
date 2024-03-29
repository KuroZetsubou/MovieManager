from time import time
from pymongo.errors import DuplicateKeyError

# sanic import
from sanic.request import Request
from sanic.response import json, BaseHTTPResponse

# project import
import config
from lib.struct.__base import db
from lib.struct.user import User, UserType
from lib.struct.booking import Booking
from lib.struct.screentime import ScreenTime
from lib.struct.screentime import Movie
from lib.utils.token import TOKEN_HEADER

# POST: /api/booking/book
async def booking_book(request: Request) -> BaseHTTPResponse:
    body = request.json
    if body.get("screenId") is None:
        return json({
            "status": 400,
            "message": "missing screenId value"
        }, status=400)
    slots = body.get("slots")
    screenTime = ScreenTime().getById(body.get("screenId"))
    now = int(time())
    usr = User().getByToken(request.headers.get(TOKEN_HEADER))

    if screenTime.screenTime - config.BOOKING_MAX_TIME_BEFORE < now:
        if usr.usertype == UserType.CLIENT:
            return json({
                "status": 500,
                "message": "cannot book now. please contact the theatre for booking."
            }, status=500)

    booking = Booking()
    booking.user = usr
    booking.screenTime = screenTime
    booking.movie = screenTime.movie
    booking.slots = [] if slots is None else slots
    try:
        _id = booking.addOnDb()
        return json({
            "status": 200,
            "message": "ok",
            "id": _id
        })
    except DuplicateKeyError:
        return json({
            "status": 500,
            "message": "you already booked for this screening"
        }, status=500)

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
    if booking.paid:
        return json({
            "status": 500,
            "message": "booking already paid"
        }, status=500)
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
            "message": "endpoint reserved for internal paying. for clients use /api/booking/pay"
        }, status=403)
    booking = Booking().getById(body.get("bookingId"))
    if booking.paid:
        return json({
            "status": 500,
            "message": "booking already paid"
        }, status=500)
    booking.pay()
    return json({
        "status": 200,
        "message": "ok"
    })