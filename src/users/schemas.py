from pydantic import BaseModel

# Users schemas

class SUserAuth(BaseModel):
    username: str
    password: str