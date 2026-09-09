from fastapi import HTTPException
from bson import ObjectId

from schemas.expenseSchema import CreateExpense, UpdateExpense
from utils.database import get_collection

expenses = get_collection("expenses")

def _serialize_expense(expense):
    expense["id"] = str(expense.pop("_id"))
    return expense


def createExpense(expense: CreateExpense):
    document = expense.model_dump()
    result = expenses.insert_one(document)
    document["_id"] = result.inserted_id
    return _serialize_expense(document)

# Description   Retrieve all expenses of a trip
# Method        GET
# Endpoint      /expenses/{trip_id}
def getAllExpensesOfTrip(tripId: int):
    return [_serialize_expense(expense) for expense in expenses.find({"trip_id": tripId})]

# Description   Retrieve particular expense
# Method        GET
# Endpoint      /expenses/{expense_id}
def _object_id(expense_id: str):
    if not ObjectId.is_valid(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return ObjectId(expense_id)


def getExpenseById(expenseId: str):
    expense = expenses.find_one({"_id": _object_id(expenseId)})
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return _serialize_expense(expense)

# Description   Update particular expense
# Method        PUT
# Endpoint      /expenses/{expense_id}
def updateExpenseById(expenseId: str, expense: UpdateExpense):
    changes = expense.model_dump(exclude_unset=True)
    result = expenses.update_one({"_id": _object_id(expenseId)}, {"$set": changes})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return getExpenseById(expenseId)

# Description   Delete particular expense
# Method        DELETE
# Endpoint      /expenses/{expense_id}
def deleteExpenseById(expenseId: str):
    result = expenses.delete_one({"_id": _object_id(expenseId)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": f"Record with id: {expenseId} is deleted"}