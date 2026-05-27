class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail
        super().__init__(detail)


class UserNotFound(BaseDatabaseException):
    pass


class UserAlreadyExists(BaseDatabaseException):
    pass


class LocationAlreadyExists(BaseDatabaseException):
    pass


class LocationNotFound(BaseDatabaseException):
    pass


class CategoryNotFound(BaseDatabaseException):
    pass


class CategoryAlreadyExists(BaseDatabaseException):
    pass


class PostNotFound(BaseDatabaseException):
    pass


class CommentNotFound(BaseDatabaseException):
    pass
