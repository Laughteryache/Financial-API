from src.dao.base import BaseDAO
from src.users.models import Users

# Module for working with Users trable (idk why I created it)

class UsersDAO(BaseDAO):
    model = Users
