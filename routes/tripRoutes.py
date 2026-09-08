from fastapi import APIRouter, Depends

router = APIRouter(prefix="/trips",tags=["Trips"])

# Creating a trip
@router.post("/")
def create_trip():
    return {
        "message" : "Trip created successfully"
    }

# Retrieve a trip
@router.get("/{id}")
def get_trip():
    return {
        "message" : "Trip Details retrieved"
    }

# Update trip details
@router.put("/{id}")
def update_trip():
    return {
        "message" : "Trip details updated"
    }

# Delete trip
@router.delete("/{id}")
def delete_trip():
    return {
        "message" : "Trip details deleted"
    }