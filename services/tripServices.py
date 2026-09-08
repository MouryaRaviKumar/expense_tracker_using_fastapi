from .expenseServices import calculate_split


def create_trip(collection, trip):
    data = trip.model_dump(exclude_none=True) if hasattr(trip, "model_dump") else dict(trip)
    data.setdefault("List_of_friends", [])
    collection.insert_one(data)
    return get_trip(collection, data["trip_id"])


def get_trip(collection, trip_id):
    trip = collection.find_one({"trip_id": trip_id})
    if trip is None:
        raise LookupError("Trip not found")
    trip["id"] = str(trip.pop("_id"))
    return trip


def update_trip(collection, trip_id, updates):
    data = updates.model_dump(exclude_unset=True) if hasattr(updates, "model_dump") else dict(updates)
    result = collection.update_one({"trip_id": trip_id}, {"$set": data})
    if result.matched_count == 0:
        raise LookupError("Trip not found")
    return get_trip(collection, trip_id)


def delete_trip(collection, trip_id):
    result = collection.delete_one({"trip_id": trip_id})
    if result.deleted_count == 0:
        raise LookupError("Trip not found")
    return True


def add_friend(collection, trip_id, friend):
    result = collection.update_one(
        {"trip_id": trip_id},
        {"$addToSet": {"List_of_friends": friend}},
    )
    if result.matched_count == 0:
        raise LookupError("Trip not found")
    return get_trip(collection, trip_id)


def trip_summary(trip_collection, expense_collection, trip_id):
    trip = get_trip(trip_collection, trip_id)
    summary = {
        friend: {"paid": 0, "share": 0, "balance": 0}
        for friend in trip.get("List_of_friends", [])
    }
    total = 0
    for expense in expense_collection.find({"trip_id": trip_id}):
        total += expense["amount"]
        person = expense["paid_by"]
        summary.setdefault(person, {"paid": 0, "share": 0, "balance": 0})
        summary[person]["paid"] += expense["amount"]
        for friend, share in calculate_split(expense)["shares"].items():
            summary.setdefault(friend, {"paid": 0, "share": 0, "balance": 0})
            summary[friend]["share"] += share
    for person in summary:
        summary[person]["balance"] = round(summary[person]["paid"] - summary[person]["share"], 2)
    return {"trip_id": trip_id, "total_expenses": total, "members": summary}