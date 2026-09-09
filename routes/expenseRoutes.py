from fastapi import APIRouter
from utils.database import get_collection

from services.expenseServices import ( 
        createExpense, 
        getAllExpensesOfTrip, 
        getExpenseById, 
        updateExpenseById, 
        deleteExpenseById
    )

from schemas.expenseSchema import (
    MessageResponse,
    CreateExpense,
    UpdateExpense,
    ExpenseResponse
)
expenses = get_collection("expenses")

router = APIRouter(prefix="/expenses",tags=["Expense"])

# Creating a Expense record
@router.post("/",response_model=ExpenseResponse, status_code=201)
def create_Expense_Record(expense: CreateExpense):
    return createExpense(expense)

# Getting all the expense records
@router.get("/trip/{trip_id}", response_model=list[ExpenseResponse], status_code=200)
def retrieve_All_Records(trip_id: int):
    return getAllExpensesOfTrip(trip_id)

# Getting a particular expense record
@router.get("/{id}", response_model=ExpenseResponse, status_code=200)
def record_By_Id(id: str):
    return getExpenseById(id)

# Updating a particular record
@router.put("/{id}", response_model=ExpenseResponse, status_code=200)
def update_Record(id: str, expense: UpdateExpense):
    return updateExpenseById(id, expense)

# Deleting a particular record
@router.delete("/{id}",response_model=MessageResponse,status_code=200)
def delete_Record(id: str):
    return deleteExpenseById(id)