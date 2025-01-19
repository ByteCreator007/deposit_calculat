import json
from datetime import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from typing import Dict

from sqlalchemy import insert
from databases import Database

from src.config import settings
from src.models import deposits

database = Database(settings.database_url)

async def calculate_deposit_logic(date_str: str, periods: int, amount: int, rate: float) -> Dict[str, float]:
    try:
        start_date = datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Invalid date")

    results = {}
    last_day_of_month = monthrange(start_date.year, start_date.month)[1]
    if start_date.day == last_day_of_month:
        amount += amount * (rate / 100) / 12
    results[start_date.strftime("%d.%m.%Y")] = round(amount, 2)

    for period in range(1, periods):
        next_date = start_date + relativedelta(months=period)
        amount += amount * (rate / 100) / 12
        results[next_date.strftime("%d.%m.%Y")] = round(amount, 2)

    return results

async def store_deposit_in_db(date_str: str, periods: int, amount: int, rate: float, results: dict) -> None:
    query = (
        insert(deposits)
        .values(
            date=date_str,
            periods=periods,
            amount=amount,
            rate=rate,
            result=json.dumps(results),
        )
    )
    await database.execute(query)

async def calculate_and_store(date_str: str, periods: int, amount: int, rate: float) -> Dict[str, float]:
    results = await calculate_deposit_logic(date_str, periods, amount, rate)
    await store_deposit_in_db(date_str, periods, amount, rate, results)
    return results
