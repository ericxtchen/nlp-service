import httpx
from app.core.config import settings
import logging
from dotenv import load_dotenv
import os 
load_dotenv()

logger = logging.getLogger(__name__)
async def fetch_transcript(bot_id: str, client: httpx.AsyncClient):
    headers = {'Authorization': f'Bearer {os.getenv("RECALL_API_KEY")}', 'Accept': 'application/json'}
    try:
        logger.info(f"Retrieving transcript with bot ID: {bot_id}")
        resp = await client.get(f"{settings.API_BASE_URL}{bot_id}", headers=headers)
        resp.raise_for_status()
        transcipt_url = await resp.json()['recordings']['media_shortcuts']['transcript']['data']['download_url']
        transcript_resp = await client.get(transcipt_url, headers=headers)
        transcript_resp.raise_for_status()
        transcript = await transcript_resp.json()
        logger.info(f"Successfully fetched transcript for bot_id: {bot_id}")
        return transcript
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching transcript: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Error fetching transcript for bot_id {bot_id}: {str(e)}")
        raise

def process_transcript(transcript: dict):
    pass