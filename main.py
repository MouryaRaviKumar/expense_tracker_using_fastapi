from fastapi import FastAPI
from contextlib import asynccontextmanager
from schemas import MessageResponse
from database import *
import database
from routes import router as expenseRouter

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

app.include_router(expenseRouter)