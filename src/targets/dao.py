from sqlalchemy import select

from sqlalchemy.exc import SQLAlchemyError

from src.dao.base import BaseDAO
from src.database import async_session
from src.targets.models import Targets
from src.utils import get_msg_exception_type
from src.logger import logger

# Module for working with the Targets table

class TargetsDAO(BaseDAO):
    model = Targets

    @classmethod
    async def find_user_targets(cls, user_id: int):
        try:
            async with async_session() as session:
                query = select(
                    Targets.id,
                    Targets.deposit_id,
                    Targets.target,
                    Targets.start_date,
                    Targets.end_date,
                    Targets.status,
                ).where(Targets.user_id == user_id)
                targets = await session.execute(query)

                return targets.mappings().all()
        
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot find user targets'
            extra = {"id": user_id}
            logger.error(msg=msg,
                         extra=extra,
                         exc_info=True)