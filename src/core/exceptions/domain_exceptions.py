class BaseDomainException(BaseException):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail

class UserNotFoundByIdException(BaseDomainException):
    _detail = 'Пользователь с id : {id} не найден'

    def __init__(self, id):
        self._detail = self._detail.format(id=id)

class UserNotFoundByUsernameException(BaseDomainException):
    _detail = 'Пользователь с username : {username} не найден'
    
    def __init__(self, username):
        self._detail = self._detail.format(username=username)


class AlreadyOccupied(BaseDomainException):
    _detail = 'Пользователь с такими данными уже существует'
    def __init__(self):
        pass
