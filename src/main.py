from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from .services import calculate_and_store, database
from .config import settings

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class DepositRequest(BaseModel):
    date: str = Field(..., regex=r"^\d{2}\.\d{2}\.\d{4}$", description="Дата в формате dd.mm.yyyy")
    periods: int = Field(..., ge=1, le=60, description="Кол-во месяцев по вкладу (1-60)")
    amount: int = Field(..., ge=10000, le=3000000, description="Сумма вклада (10k - 3kk)")
    rate: float = Field(..., ge=1, le=8, description="Процентная ставка (1-8)")

@app.post("/calculate")
async def calculate_deposit(request: DepositRequest) -> Dict[str, float]:
    try:
        results = await calculate_and_store(
            request.date,
            request.periods,
            request.amount,
            request.rate
        )
        return results

    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты")