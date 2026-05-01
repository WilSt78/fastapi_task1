class BaseDatabaseException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail

class EmailIsOccupied(BaseDatabaseException):
    _detail = 'Пользователь с email : {email} уже существует'

    def __init__(self, email):
        self._detail = self._detail.format(email=email)

class UsernameIsOccupied(BaseDatabaseException):
    _detail = 'Пользователь с username : {username} уже существует'

    def __init__(self, username):
        self._detail = self._detail.format(username=username)

class UserNotFoundById(BaseDatabaseException):
    _detail = 'Пользователь с id : {id} не найден'

    def __init__(self, id):
        self._detail = self._detail.format(id=id)


class UserNotFoundByUsername(BaseDatabaseException):
    _detail = 'Пользователь с username : {username} не найден'

    def __init__(self, username):
        self._detail = self._detail.format(username=username)


