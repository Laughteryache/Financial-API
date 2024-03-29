from enum import Enum

from pydantic import BaseModel

# Deposits schemas

class Currency(Enum):

    USD = "USD"
    EUR = "EUR"
    YUAN = "YUAN"
    RUB = "RUB"


class SResult(BaseModel):

    result: str


class SMyDeposits(BaseModel):

    id: int
    name: str
    currency: Currency
    current_balance: int
    history: list[int]


class STransactionAdded(BaseModel):

    current_balance: int
    currency: str
    history: list[int]


class SAddDeposit(BaseModel):

    name: str
    currency: Currency
