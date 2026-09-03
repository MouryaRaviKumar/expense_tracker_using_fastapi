from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class MessageResponse(BaseModel):
    message: str

class ExpenseBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Title of the expense"
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Expense amount must be greater than 0"
    )
    timestamp: datetime = Field(
        ...,
        description="Date and time when the expense occurred"
    )
    note: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional note about the expense"
    )

class CreateExpense(ExpenseBase):
    pass

class UpdateExpense(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100
    )
    amount: Optional[float] = Field(
        None,
        gt=0
    )
    timestamp: Optional[datetime] = None
    note: Optional[str] = Field(
        None,
        max_length=500
    )

class ExpenseResponse(ExpenseBase):
    id: str