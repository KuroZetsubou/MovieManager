# API Docs

In order to use the API, you need to retreive from server a token (can be done on `user/login`)

## Create a User

### `POST: /user/makeAccount`

```json
{
    "username": "user",
    "password": "secret"
}
```

### `POST: /user/login`

#### Request
```json
{
    "username": "user",
    "password": "secret",
}
```

#### Response
```json
{
    "token": "AAAAAAAA==" // this will be needed for other endpoints
}
```

Token must be put as a dedicated header on your HTTP request, `X-Token`.

## Book a screening

### `GET: /screens/getAll`

#### Response

```json
{
    "screens": [
		{
			"id": "d5f63ed97c4ab1cf687ffa7e3cf270b8288244b0ca55d74e0277b01e738002a1",
			"screenTime": 1694917910,
			"capacity": 300,
			"movie": {
				"movieName": " Risvegli",
				"omdbName": " Risvegli"
			}
		}
    ]
}
```

- Take the `screens.id` value and put it on the next request

### `POST: /booking/book`

#### Request

```json
{
    "screenId": "d5f63ed97c4ab1cf687ffa7e3cf270b8288244b0ca55d74e0277b01e738002a1"
}
```

- You can see all your bookings (included the IDs) via `/user/getBookings` (it's a `GET` endpoint)

## Pay a booking

There are two ways for paying the booking, one from the client side, one from employee/admin side. Client side is supposed to have a check from the external payment system, meanwhile employee one, since it's operated locally (cash/card) at the teathre, there won't be any check.

### POST: /api/booking/pay (client)
### POST: /api/booking/internalPayment (employee/admin)

#### Request
```json
{
	"bookingId": "<bookingId>"
}
```

> In case of mismatching user type for the scope

```json
{
	"status": 403,
	"message": "endpoint reserved for clients paying. for employee use /api/booking/internalPayment"
}
```
```json
{
	"status": 403,
	"message": "endpoint reserved for internal paying. for clients use /api/booking/pay"
}
```