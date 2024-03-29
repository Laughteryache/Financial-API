from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.config import settings
from src.users.dao import UsersDAO

# Module with user authentication functions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: SyntaxWarning) -> str:
    
    # Function hashes user's password
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    # Function checks entered password and hashed password from database
    
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    
    # Function creates access token
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    
    # Function authenticates user if user exits and enters correct password
    
    user = await UsersDAO.find_one_or_none(username=username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
