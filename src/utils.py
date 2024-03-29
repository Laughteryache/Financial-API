from sqlalchemy.exc import SQLAlchemyError

# Module for utils

async def access_to(model, user_id: int, requested_id: int) -> bool:
    
    # Function checks user's access to an object

    user_ids = await model.get_user_ids(user_id=user_id)

    if requested_id in user_ids:
        return True

    return False


async def get_msg_exception_type(exception) -> str:
    
    # Function throws type of exception
    
    if isinstance(exception, SQLAlchemyError):
        msg = 'Database Exc'
        
    elif isinstance(exception, Exception):
        msg = 'Unknown Exc'
        
    return msg