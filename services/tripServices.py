
from fastapi import HTTPException
from bson import ObjectId

from schemas.tripSchema import CreateTrip, UpdateTrip
from utils.database import get_collection

trips = get_collection("trips")


def _serialize_trip(trip):
    trip["id"] = str(trip.pop("_id"))
    return trip


def create_trip(trip: CreateTrip):
    document = trip.model_dump()
    result = trips.insert_one(document)
    document["_id"] = result.inserted_id
    return _serialize_trip(document)

# Description   Retrieve a trip
# Method        GET
# Endpoint      /trips/{id}
def get_trip(id: int):
    trip = trips.find_one({"trip_id": id})
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return _serialize_trip(trip)

# Description   Update trip details
# Method        PUT
# Endpoint      /trips/{id}
def update_trip(id: int, trip: UpdateTrip):
    changes = trip.model_dump(exclude_unset=True)
    result = trips.update_one({"trip_id": id}, {"$set": changes})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    return get_trip(id)

# Description   Delete trip details
# Method        DELETE
# Endpoint      /trips/{id}
def delete_trip(id: int):
    result = trips.delete_one({"trip_id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message": "Trip details deleted"}