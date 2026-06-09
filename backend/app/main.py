from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import extract
from datetime import date
import time

from .database import engine, SessionLocal
from .models import Base, CurrencyRate
from .services import fetch_rates_from_nbp
from .schemas import CurrencyRateResponse

app = FastAPI(
    title="Currency Rates API",
    version="1.0.0"
)

@app.on_event("startup")
def startup():

    for _ in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected")
            break

        except Exception:
            print("Waiting for database...")
            time.sleep(3)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Currency Rates API is running"
    }

@app.post("/currencies/fetch")
def fetch_currencies():

    db: Session = SessionLocal()

    try:
        data = fetch_rates_from_nbp()

        saved = 0

        for rate in data["rates"]:

            currency_rate = CurrencyRate(
                currency=rate["currency"],
                code=rate["code"],
                rate=rate["mid"],
                rate_date=datetime.strptime(
                    data["effectiveDate"],
                    "%Y-%m-%d"
                ).date()
            )

            db.add(currency_rate)
            saved += 1

        db.commit()

        return {
            "message": "Rates downloaded successfully",
            "saved": saved
        }

    finally:
        db.close()

@app.get(
    "/currencies",
    response_model=list[CurrencyRateResponse]
)
def get_currencies():

    db = SessionLocal()

    try:
        return db.query(CurrencyRate).all()

    finally:
        db.close()

@app.get(
    "/currencies/date/{rate_date}",
    response_model=list[CurrencyRateResponse]
)
def get_currencies_by_date(rate_date: date):

    db = SessionLocal()

    try:
        return (
            db.query(CurrencyRate)
            .filter(CurrencyRate.rate_date == rate_date)
            .all()
        )

    finally:
        db.close()

@app.get("/currencies/years")
def get_years():

    db = SessionLocal()

    try:

        years = (
            db.query(
                extract("year", CurrencyRate.rate_date)
            )
            .distinct()
            .all()
        )

        return [
            int(year[0])
            for year in years
        ]

    finally:
        db.close()

@app.get("/currencies/months")
def get_months():

    db = SessionLocal()

    try:

        months = (
            db.query(
                extract("month", CurrencyRate.rate_date)
            )
            .distinct()
            .all()
        )

        return [
            int(month[0])
            for month in months
        ]

    finally:
        db.close()

@app.get("/currencies/quarters")
def get_quarters():

    db = SessionLocal()

    try:

        quarters = (
            db.query(
                (
                    (
                        extract(
                            "month",
                            CurrencyRate.rate_date
                        ) - 1
                    ) / 3
                ) + 1
            )
            .distinct()
            .all()
        )

        return [
            int(q[0])
            for q in quarters
        ]

    finally:
        db.close()