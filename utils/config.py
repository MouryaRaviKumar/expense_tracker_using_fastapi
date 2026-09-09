import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.__MONGO_URI = os.getenv("MONGO_URI")
        self.__DB_NAME = os.getenv("DB_NAME")
        self.__TRIP_COLLECTION = os.getenv("TRIP_COLLECTION")
        self.__EXPENSE_COLLECTION = os.getenv("EXPENSE_COLLECTION")

    @property
    def MONGO_URI(self):
        return self.__MONGO_URI

    @property
    def DB_NAME(self):
       return self.__DB_NAME

    @property
    def TRIP_COLLECTION(self):
        return self.__TRIP_COLLECTION

    @property
    def EXPENSE_COLLECTION(self):
        return self.__EXPENSE_COLLECTION

settings = Settings()