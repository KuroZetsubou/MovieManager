

class BookingNotFoundException(Exception):
    """Exception raised for booking not found on database

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)