from sqlalchemy import select, update

from sqlalchemy.exc import SQLAlchemyError

from src.dao.base import BaseDAO
from src.database import async_session
from src.deposits.models import Deposits
from src.utils import get_msg_exception_type
from src.logger import logger

# Module for working with the Deposits table

class DepositsDAO(BaseDAO):
    model = Deposits

    @classmethod
    async def find_user_deposits(cls, user_id: int):
        try:
            async with async_session() as session:
                query = select(
                    Deposits.id,
                    Deposits.name,
                    Deposits.currency,
                    Deposits.current_balance,
                    Deposits.history,
                ).where(Deposits.user_id == user_id)
                deposits = await session.execute(query)
                return deposits.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ": Cannot find user's deposits"
            extra = {'user_id': id}
            logger.error(msg = msg,
                         extra = extra,
                         exc_info = True)

    @classmethod
    async def add_transaction(cls, id: int, amount: int):
        try:
            async with async_session() as session:
                query = select(
                    Deposits.current_balance, Deposits.currency, Deposits.history
                ).where(Deposits.id == id)

                result = await session.execute(query)
                data = result.first()

                if data:
                    current_balance, currency, history = data

                    changed_balance = current_balance + amount
                    changed_history = history + [amount]

                query = (
                    update(Deposits)
                    .where(Deposits.id == id)
                    .values(current_balance=changed_balance, history=changed_history)
                )
                await session.execute(query)
                await session.commit()

                return {
                    "current_balance": changed_balance,
                    "currency": currency,
                    "history": changed_history,
                }
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ": Cannot add transaction"
            extra = {'deposit_id': id,
                     'amount': amount}
            logger.error(msg = msg,
                         extra = extra,
                         exc_info = True)
            