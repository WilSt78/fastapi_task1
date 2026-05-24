from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain.use_cases.auth import GetCurrentUserUseCase
from src.core.exceptions.domain_exceptions import InvalidTokenException, UserNotFoundByUsernameException
from src.schemas.Users import UserResponse

security = HTTPBearer()

async def get_current_user( 
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserResponse:
    use_case = GetCurrentUserUseCase()
    
    try:
        user = await use_case.execute(credentials.credentials)  
        return user
    except (InvalidTokenException, UserNotFoundByUsernameException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.get_detail(),
            headers={"WWW-Authenticate": "Bearer"},
        )