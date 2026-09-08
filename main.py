from fastapi import FastAPI
from contextlib import asynccontextmanager
from schemas.expenseSchema import MessageResponse
from utils.database import *
import utils.database as database
from routes import tripRoutes, expenseRoutes

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Starting Server")
    print("Connecting to Database")
    database.connect()
    print("Connected to Database")
    yield
    print("Disconnecting to Databse")
    database.disconnect()
    print("Database Disconnected")
    print("Shutting Down Server")

app = FastAPI(lifespan=lifespan)

@app.get("/health",response_model=MessageResponse)
def health():
    return{
        "message":"Application Working Successfully"
    }

app.include_router(tripRoutes.router)
app.include_router(expenseRoutes.router)