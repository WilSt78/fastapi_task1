from ..domain.use_cases.users import GetAllUsersUseCase, GetUserByIdUseCase, \
GetUserByUsernameUseCase, UpdateUserUseCase,\
DeleteUserUseCase, CreateUserUseCase
from ..domain.use_cases.auth import AuthenticateUserUseCase, CreateAccessTokenUseCase, GetCurrentUserUseCase


def get_all_users_use_case() -> GetAllUsersUseCase:
    return GetAllUsersUseCase()

def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()

def get_user_by_username_use_case() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()

def update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase()

def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()

def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()

def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()

def create_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()

def get_current_user_use_case() -> GetCurrentUserUseCase:
    return GetCurrentUserUseCase()