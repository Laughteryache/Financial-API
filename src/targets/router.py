from datetime import date

from fastapi import APIRouter, Depends

from src.deposits.dao import DepositsDAO
from src.deposits.schemas import SResult
from src.exceptions import NoAccessToException
from src.targets.dao import TargetsDAO
from src.targets.schemas import SAddTarget, STarget
from src.users.dependencies import get_current_user
from src.users.models import Users
from src.utils import access_to

# Targets router

router = APIRouter(prefix="/targets",
                   tags=["Targets"])


@router.post("/add", response_model=SResult)
async def add_target(target: SAddTarget, user: Users = Depends(get_current_user)):

    access = await access_to(
        model=DepositsDAO, user_id=user.id, requested_id=target.deposit_id
    )

    if not access:
        raise NoAccessToException

    await TargetsDAO.add(
        user_id=user.id,
        deposit_id=target.deposit_id,
        target=target.target,
        end_date=target.end_date,
    )

    return {"result": "success"}


@router.get("/my", response_model=list[STarget])
async def get_user_targets(user: Users = Depends(get_current_user)):
    return await TargetsDAO.find_user_targets(user_id=user.id)


@router.patch("/change_target", response_model=SResult)
async def change_user_target(
    target_id: int, new_target: str, user: Users = Depends(get_current_user)
):

    access = await access_to(model=TargetsDAO, user_id=user.id, requested_id=target_id)

    if not access:
        raise NoAccessToException

    await TargetsDAO.change(id=target_id, target=new_target)

    return {"result": "success"}


@router.patch("/change_status", response_model=SResult)
async def change_user_target_status(
    target_id: int, status: bool, user: Users = Depends(get_current_user)
):

    access = await access_to(model=TargetsDAO, user_id=user.id, requested_id=target_id)

    if not access:
        raise NoAccessToException

    await TargetsDAO.change(id=target_id, status=status)

    return {"result": "success"}


@router.patch("/change_date", response_model=SResult)
async def change_user_target_status(
    target_id: int, new_date: date, user: Users = Depends(get_current_user)
):

    access = await access_to(model=TargetsDAO, user_id=user.id, requested_id=target_id)

    if not access:
        raise NoAccessToException

    await TargetsDAO.change(id=target_id, end_date=new_date)

    return {"result": "success"}


@router.delete("/delete", response_model=SResult)
async def delete_user_target(target_id: int, user: Users = Depends(get_current_user)):

    access = await access_to(model=TargetsDAO, user_id=user.id, requested_id=target_id)

    if not access:
        raise NoAccessToException

    await TargetsDAO.delete(id=target_id)

    return {"result": "success"}
