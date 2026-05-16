
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.Token import Token
from src.domain.use_cases.auth import AuthenticateUserUseCase, CreateAccessTokenUseCase
from src.core.exceptions.domain_exceptions import UserNotFoundByUsernameException, PasswordsDoesntMatch
from src.api.depends import create_token_use_case, authenticate_user_use_case

router = APIRouter(prefix='/auth',tags=['Аутентификация'])


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: AuthenticateUserUseCase = Depends(authenticate_user_use_case),
    create_token_use_case: CreateAccessTokenUseCase = Depends(create_token_use_case), 
) -> Token:
    try:
        user = use_case.execute(form_data.username, form_data.password)
    except PasswordsDoesntMatch as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.get_detail(),
        )
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=e.get_detail()
        )

    access_token = create_token_use_case.execute(user.username)
    return Token(access_token=access_token, token_type="bearer")