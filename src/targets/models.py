from datetime import datetime

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String

from src.database import Base

# Formation Targets table

class Targets(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    deposit_id = Column(ForeignKey("deposits.id"))
    target = Column(String, nullable=False)
    start_date = Column(Date, default=datetime.utcnow())
    end_date = Column(Date)
    status = Column(Boolean, default=False)
