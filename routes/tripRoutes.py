from fastapi import APIRouter, Depends

from services.tripServices import (
    create_trip,
    get_trip,
    update_trip,
    delete_trip
)

from schemas.tripSchema import (
    CreateTrip,
    UpdateTrip,
    TripResponse,
    MessageResponse
)

router = APIRouter(prefix="/trips", tags=["Trips"])


# Creating a trip
@router.post("/", response_model=TripResponse, status_code=201)
def create_trip_route(trip: CreateTrip):
    return create_trip(trip)


# Retrieve a trip
@router.get("/{id}", response_model=TripResponse, status_code=200)
def get_trip_route(id: int):
    return get_trip(id)


# Update trip details
@router.put("/{id}", response_model=TripResponse, status_code=200)
def update_trip_route(id: int, trip: UpdateTrip):
    return update_trip(id, trip)


# Delete trip
@router.delete("/{id}", response_model=MessageResponse, status_code=200)
def delete_trip_route(id: int):
    return delete_trip(id)