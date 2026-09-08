import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.__MONGO_URI = os.getenv("MONGO_URI")
        self.__DB_NAME = os.getenv("DB_NAME")
        self.__COLLECTION_NAME = os.getenv("COLLECTION_NAME")

    @property
    def MONGO_URI(self):
        return self.__MONGO_URI

    @property
    def DB_NAME(self):
       return self.__DB_NAME

    @property
    def COLLECTION_NAME(self):
        return self.__COLLECTION_NAME

settings = Settings()