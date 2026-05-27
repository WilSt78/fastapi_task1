from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.depends import (
    authenticate_user_use_case,
    create_access_token_use_case,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    WrongPasswordException,
)
from src.domain.use_cases.auth import (
    AuthenticateUseCase,
    CreateAccessTokenUseCase,
)

from src.schemas.auth import Token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        AuthenticateUseCase, Depends(authenticate_user_use_case)
    ],
    create_token_use_case: CreateAccessTokenUseCase = Depends(
        create_access_token_use_case
    ),
) -> Token:
    try:
        user = await auth_use_case.execute(
            username=data.username, password=data.password
        )
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.detail
        ) from exc

    access_token = await create_token_use_case.execute(
        username=user.username
    )

    return Token(access_token=access_token, token_type="bearer")
