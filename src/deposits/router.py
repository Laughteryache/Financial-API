from fastapi import APIRouter, Depends
from fastapi_versioning import version

from src.deposits.dao import DepositsDAO
from src.deposits.schemas import (SAddDeposit, SMyDeposits, SResult,
                                  STransactionAdded)
from src.exceptions import NoAccessToException
from src.users.dependencies import get_current_user
from src.users.models import Users
from src.utils import access_to

# Deposits router

router = APIRouter(prefix="/deposits", 
                   tags=["Deposits"])


@router.post("/add", response_model=SResult)
@version(1)
async def add_deposit(deposit_data: SAddDeposit, user=Depends(get_current_user)):
    await DepositsDAO.add(
        name=deposit_data.name, currency=deposit_data.currency.value, user_id=user.id
    )

    return {"result": "success"}


@router.get("/my", response_model=list[SMyDeposits])
async def get_user_deposits(user: Users = Depends(get_current_user)):
    return await DepositsDAO.find_user_deposits(user_id=user.id)


@router.post("/transaction", response_model=STransactionAdded)
async def transaction(
    deposit_id: int, amount: int, user: Users = Depends(get_current_user)
):

    access = await access_to(
        model=DepositsDAO, user_id=user.id, requested_id=deposit_id
    )

    if not access:
        raise NoAccessToException

    return await DepositsDAO.add_transaction(id=deposit_id, amount=amount)


@router.patch("/change_name", response_model=SResult)
async def change_deposit_name(
    deposit_id: int, new_name: str, user: Users = Depends(get_current_user)
):

    access = await access_to(
        model=DepositsDAO, user_id=user.id, requested_id=deposit_id
    )

    if not access:
        raise NoAccessToException

    await DepositsDAO.change(id=deposit_id, name=new_name)

    return {"result": "success"}


@router.delete("/delete", response_model=SResult)
async def delete_deposit(deposit_id: int, user: Users = Depends(get_current_user)):

    access = await access_to(
        model=DepositsDAO, user_id=user.id, requested_id=deposit_id
    )

    if not access:
        raise NoAccessToException

    await DepositsDAO.delete(id=deposit_id)

    return {"result": "success"}
