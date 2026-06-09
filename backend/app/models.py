from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from .database import Base


class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)

    currency = Column(String, nullable=False)
    code = Column(String, nullable=False)

    rate = Column(Float, nullable=False)

    rate_date = Column(Date, nullable=False)