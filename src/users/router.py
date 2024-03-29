from fastapi import APIRouter, Depends, Response

from src.deposits.schemas import SResult
from src.exceptions import (IncorrectLoginDataException,
                            IncorrectPasswordException,
                            UserAlreadyExistsException, UsernameIsTakenException)
from src.users.auth import (authenticate_user, create_access_token,
                            get_password_hash, verify_password)
from src.users.dao import UsersDAO
from src.users.dependencies import get_current_user
from src.users.models import Users
from src.users.schemas import SUserAuth

# Users router

router = APIRouter(prefix="/user",
                   tags=["Auth & Users"])


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(username=user_data.username)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(username=user_data.username, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(
        username=user_data.username, password=user_data.password
    )
    if not user:
        raise IncorrectLoginDataException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)

    return {"access_token": access_token}


@router.patch("/change_username", response_model=SResult)
async def change_username(new_username: str, user: Users = Depends(get_current_user)):
    username_is_taken = await UsersDAO.find_one_or_none(username=new_username)
    
    if username_is_taken:
        raise UsernameIsTakenException
    
    await UsersDAO.change(id = user.id, username=new_username)
    return {'result': 'success'}


@router.post("/change_password", response_model=SResult)
async def change_password(
    old_password: str, new_password: str, user: Users = Depends(get_current_user)
):
    password_is_valid = verify_password(old_password, user.hashed_password)

    if not password_is_valid:
        raise IncorrectPasswordException

    hashed_password = get_password_hash(new_password)
    await UsersDAO.change(id=user.id, hashed_password=hashed_password)
    return {'result': 'success'}


@router.get("/logout")
async def logout_user(response: Response, user: Users = Depends(get_current_user)):

    response.delete_cookie(key="access_token", httponly=True)
