from src.logger import logger
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session
from src.utils import get_msg_exception_type

# Module for general works with tables

class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, id: int):
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(id=id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot find by id'
            extra = {
                "id": id
            }
            logger.error(msg=msg,
                         extra=extra,
                         exc_info=True)
            

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot find'
            extra = filter_by
            logger.error(msg = msg,
                         extra=extra,
                         exc_info=True)
            
            

    @classmethod
    async def find_by_filter(cls, **filter_by):
        try:
            async with async_session() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot find by filter'
            extra = filter_by
            logger.error(msg = msg,
                         extra=extra,
                         exc_info=True)
            

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session() as session:
                query = insert(cls.model).values(**data)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot add'
            extra = data
            logger.error(msg=msg,
                         extra=extra,
                         exc_info=True)
                
            

    @classmethod
    async def change(cls, id: int, **changes):
        try:
            async with async_session() as session:
                query = update(cls.model).where(cls.model.id == id).values(**changes)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot change'
            extra = changes
            logger.error(msg=msg,
                         extra=extra,
                         exc_info=True)


    @classmethod
    async def delete(cls, id: int):
        try:
            async with async_session() as session:
                query = delete(cls.model).where(cls.model.id == id)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot delete'
            extra = {"id": id}
            logger.error(msg=msg,
                         extra=extra,
                         exc_info=True)


    @classmethod
    async def get_user_ids(cls, user_id: int):
        try:
            async with async_session() as session:
                query = select(cls.model.id).where(cls.model.user_id == user_id)

                results_ids = await session.execute(query)

                if not results_ids:
                    return []

                results_ids = results_ids.mappings().all()
                results_ids = list(map(lambda x: x["id"], results_ids))

                return results_ids
        except (SQLAlchemyError, Exception) as e:
            msg = await get_msg_exception_type(e) + ': Cannot delete'
            extra = {"id": user_id}
            logger.error(msg=msg,
                         extra=extra,
                         exc_info=True)
