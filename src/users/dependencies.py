from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from src.config import settings
from src.exceptions import (InvalidTokenException, TokenNotFoundedException,
                            UserNotFoundedException)
from src.users.dao import UsersDAO

# Module for dependencies

def get_token(request: Request):
    
    # Function gets access token from cookies and returns it
    
    token = request.cookies.get("access_token")

    if not token:
        raise TokenNotFoundedException

    return token


async def get_current_user(token: str = Depends(get_token)):
    
    # Function checks current user
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    except JWTError:
        raise InvalidTokenException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise InvalidTokenException

    user_id: str = payload.get("sub")
    if not user_id:
        raise InvalidTokenException

    user = await UsersDAO.find_by_id(int(user_id))

    if not user:
        raise UserNotFoundedException

    return user
