import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://api.example.com/transcripts/")

settings = Settings()