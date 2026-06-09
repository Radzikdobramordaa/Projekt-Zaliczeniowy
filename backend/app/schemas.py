from datetime import date

from pydantic import BaseModel


class CurrencyRateResponse(BaseModel):
    id: int
    currency: str
    code: str
    rate: float
    rate_date: date

    class Config:
        from_attributes = True