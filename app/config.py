from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    MONGODB_URI = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("MONGODB_DATABASE")
    COLLECTION_NAME = os.getenv("MONGODB_COLLECTION")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
