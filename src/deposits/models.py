from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String

from src.database import Base

# Formation Deposits table

class Deposits(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id"))
    currency = Column(String, nullable=False)
    current_balance = Column(Integer, default=0)
    history = Column(ARRAY(item_type=Integer), default=[])
