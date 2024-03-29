from datetime import date
from typing import Optional

from pydantic import BaseModel

# Targets schemas

class SAddTarget(BaseModel):

    deposit_id: int
    target: str
    end_date: Optional[date] = None


class STarget(BaseModel):

    id: int
    deposit_id: int
    target: str
    start_date: date
    end_date: date
    status: bool
