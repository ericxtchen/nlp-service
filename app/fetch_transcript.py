import requests
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_transcript(bot_id: str):
    RECALL_API_KEY = os.getenv("RECALL_API_KEY")
    headers = {"Authorization": f"Bearer {RECALL_API_KEY}",
               "Accept": "application/json"}
    response = requests.get(f"https://us-west-2.recall.ai/api/v1/bot/{bot_id}", headers=headers)
