from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class TripBase(BaseModel):
    trip_id: int = Field(
        ...,
        gt=0,
        description="ID of the trip"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the trip"
    )
    start_date: datetime = Field(
        ...,
        description="Start date of the trip"
    )
    end_date: datetime = Field(
        ...,
        description="End date of the trip"
    )
    destination: Optional[str] = Field(
        None,
        max_length=200,
        description="Destination of the trip"
    )
    List_of_friends: Optional[list] = Field(
        None,
        description="List of friends associated with the trip"
    )

class CreateTrip(TripBase):
    pass

class UpdateTrip(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100
    )
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    destination: Optional[str] = Field(
        None,
        max_length=200
    )
    List_of_friends: Optional[list] = None

class TripResponse(TripBase):
    id: str

class MessageResponse(BaseModel):
    message: str