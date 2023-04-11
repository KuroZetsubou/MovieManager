

class UserExistsException(Exception):
    def __init__(self, username: str, *args: object) -> None:
        self.username = username
        super().__init__(*args)