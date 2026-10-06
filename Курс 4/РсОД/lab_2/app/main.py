from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Header, HTTPException, Query, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "transactions_api.json"


class TransactionBase(BaseModel):
    org_id: int
    date: str
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)


class TransactionCreate(TransactionBase):
    transaction_id: Optional[int] = None


class TransactionPatch(BaseModel):
    org_id: Optional[int] = None
    date: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    currency: Optional[str] = Field(default=None, min_length=3, max_length=3)


class Transaction(TransactionBase):
    transaction_id: int


app = FastAPI(
    title="Учебный REST API для лабораторной работы",
    version="1.0.0",
)


def load_transactions() -> List[dict]:
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


transactions: List[dict] = load_transactions()


def find_transaction(transaction_id: int) -> dict:
    for transaction in transactions:
        if transaction["transaction_id"] == transaction_id:
            return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")


@app.get("/api/transactions", response_model=List[Transaction])
def get_transactions(
    org_id: Optional[int] = Query(default=None),
    currency: Optional[str] = Query(default=None),
    x_student_tag: Optional[str] = Header(default=None),
) -> List[dict]:
    result = transactions
    if org_id is not None:
        result = [item for item in result if item["org_id"] == org_id]
    if currency is not None:
        result = [item for item in result if item["currency"].upper() == currency.upper()]
    return result


@app.head("/api/transactions", include_in_schema=False)
def head_transactions() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@app.get("/api/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int) -> dict:
    return find_transaction(transaction_id)


@app.post("/api/transactions", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate) -> dict:
    next_id = max((item["transaction_id"] for item in transactions), default=1000) + 1
    transaction = payload.model_dump()
    transaction["transaction_id"] = transaction["transaction_id"] or next_id
    transactions.append(transaction)
    return transaction


@app.put("/api/transactions/{transaction_id}", response_model=Transaction)
def replace_transaction(transaction_id: int, payload: TransactionBase) -> dict:
    transaction = find_transaction(transaction_id)
    transaction.update(payload.model_dump())
    return transaction


@app.patch("/api/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, payload: TransactionPatch) -> dict:
    transaction = find_transaction(transaction_id)
    transaction.update({key: value for key, value in payload.model_dump(exclude_unset=True).items() if value is not None})
    return transaction


@app.delete("/api/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int) -> Response:
    transaction = find_transaction(transaction_id)
    transactions.remove(transaction)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/api/redirect", include_in_schema=False)
def redirect_to_transactions() -> RedirectResponse:
    return RedirectResponse(url="/api/transactions", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
