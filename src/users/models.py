from sqlalchemy import Column, Integer, String

from src.database import Base

# Formation Users table

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
