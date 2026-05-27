from fastapi import HTTPException, status


class BaseDomainException(HTTPException):
    def __init__(
        self, detail: str, status_code: int = status.HTTP_409_CONFLICT
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.detail = detail


class PermissionDeniedException(BaseDomainException):
    _exception_text_template = (
        "Пользователь не имеет прав на это действие"
    )

    def __init__(self) -> None:
        self._exception_text_template = (
            self._exception_text_template.format()
        )
        super().__init__(detail=self._exception_text_template)


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с id='{id}' не найден в системе"
    )

    def __init__(self, id: int) -> None:
        self._exception_text_template = (
            self._exception_text_template.format(id=id)
        )
        super().__init__(detail=self._exception_text_template)


class UserNotFoundByEmailException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с email='{email}' не найден в системе"
    )

    def __init__(self, email: str) -> None:
        self._exception_text_template = (
            self._exception_text_template.format(email=email)
        )
        super().__init__(detail=self._exception_text_template)


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с username='{username}' не найден в системе"
    )

    def __init__(self, username: str) -> None:
        self._exception_text_template = (
            self._exception_text_template.format(username=username)
        )
        super().__init__(detail=self._exception_text_template)


class EmailIsOccupiedException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с email='{email}' уже зарегистрирован"
    )

    def __init__(self, email: str) -> None:
        detail = self._exception_text_template.format(email=email)
        super().__init__(detail=detail)


class UsernameIsOccupiedException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с username='{username}' уже зарегистрирован"
    )

    def __init__(self, username: str) -> None:
        detail = self._exception_text_template.format(
            username=username
        )
        super().__init__(detail=detail)


class WrongPasswordException(BaseDomainException):
    _exception_text_template = "Введенный пароль неверный"

    def __init__(self) -> None:
        detail = self._exception_text_template.format()
        super().__init__(detail=detail)


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = (
        "Локация с id = {location_id} не найдена"
    )

    def __init__(self, location_id: int) -> None:
        detail = self._exception_text_template.format(
            location_id=location_id
        )
        super().__init__(detail=detail)


class LocationNotFoundByNameException(BaseDomainException):
    _exception_text_template = (
        "Локация с названием: {locaion_name} не найдена"
    )

    def __init__(self, name: int) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail)


class LocationNameIsOccupiedException(BaseDomainException):
    _exception_text_template = (
        "Локация с названием: {location_name} уже занята"
    )

    def __init__(self, name: str) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = (
        "Категория с id = {category_id} не найдена"
    )

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(
            category_id=category_id
        )
        super().__init__(detail=detail)


class CategoryNotFoundByNameException(BaseDomainException):
    _exception_text_template = (
        "Категория с названием = {title} не найдена"
    )

    def __init__(self, title: str) -> None:
        detail = self._exception_text_template.format(title=title)
        super().__init__(detail=detail)


class CategorySlugIsOccupiedException(BaseDomainException):
    _exception_text_template = (
        "Категория с slug {slug} уже существует"
    )

    def __init__(self, slug: str) -> None:
        detail = self._exception_text_template.format(slug=slug)
        super().__init__(detail=detail)


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = (
        "Пост с id='{post_id}' не найден в системе"
    )

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail)


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = (
        "Комментарий с id='{comment_id}' не найден в системе"
    )

    def __init__(self, comment_id: int) -> None:
        detail = self._exception_text_template.format(
            comment_id=comment_id
        )
        super().__init__(detail=detail)


class PostNotFoundByAuthorException(BaseDomainException):
    _exception_text_template = (
        "Пост у автора с id='{author_id}' не найден"
    )

    def __init__(self, author_id: int) -> None:
        detail = self._exception_text_template.format(
            author_id=author_id
        )
        super().__init__(detail=detail)


class CommentNotFoundByPostException(BaseDomainException):
    _exception_text_template = (
        "Комментарий у поста с id='{post_id}' не найден"
    )

    def __init__(self) -> None:
        detail = self._exception_text_template.format()
        super().__init__(detail=detail)
