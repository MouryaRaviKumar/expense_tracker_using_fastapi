from fastapi import APIRouter

router = APIRouter(prefix="/expense",tags=["Expense"])

# Creating a Expense record
@router.post("/",status_code=201)
def create_Expense_Record():
    return{
        "message" : "Expense Record created successfully"
    }

# Getting all the expense records
@router.get("/",status_code=200)
def retrieve_All_Records():
    return{
        "message" : "All Expense Records are Retrieved"
    }

# Getting a particular expense record
@router.get("/{id}",status_code=200)
def record_By_Id(id : int):
    return{
        "message" : f"Record with id : {id} is retrieved"
    }

# Updating a particular record
@router.put("/id",status_code=200)
def update_Record(id : int):
    return{
        "message":f"Record with id : {id} is updated"
    }

# Deleting a particular record
@router.delete("/id",status_code=200)
def delete_Record(id : int):
    return{
        "message" : f"Record with id : {id} is deleted"
    }