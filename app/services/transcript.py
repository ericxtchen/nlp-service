import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
async def fetch_transcript(bot_id: str, client: httpx.AsyncClient):
    try:
        logger.info(f"Retrieving transcript with bot ID: {bot_id}")
        resp = await client.get(f"{settings.API_BASE_URL}{bot_id}")
        resp.raise_for_status()
        logger.info(f"Successfully fetched transcript for bot_id: {bot_id}")
        return resp.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching transcript: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Error fetching transcript for bot_id {bot_id}: {str(e)}")
        raise

def process_transcript(transcript: dict):
    pass