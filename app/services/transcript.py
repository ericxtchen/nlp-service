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
        print(f"BOT ID: {bot_id}")
        resp = await client.get(f"http://mock:5000/api/v1/bot/{bot_id}", headers=headers)
        resp.raise_for_status()
        transcript_json = resp.json()
        
        transcript_url = transcript_json['recordings'][0]['media_shortcuts']['transcript']['data']['download_url']
        transcript_resp = await client.get(transcript_url, headers=headers)
        transcript_resp.raise_for_status()
        transcript = transcript_resp.json()
        logger.info(f"Successfully fetched transcript for bot_id: {bot_id}")
        return transcript
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching transcript: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Error fetching transcript for bot_id {bot_id}: {str(e)}")
        raise
def transcript_to_text(transcript) -> str:
    text_segments = []
    #print(f"transcript: {transcript}")
    try:
        for entry in transcript:
            participant = entry.get("participant", {})
            name = participant.get("name") or participant.get("email") or "Unknown"
            words = entry.get("words", [])
            segment = f"{name}: " + " ".join(word.get("text", "") for word in words)
            text_segments.append(segment)
        return "\n".join(text_segments)
    except Exception as e:
        logger.error(f"Error converting transcript to text: {str(e)}")
        raise
def process_transcript(text: str):
    from main import app
    nlp_model = app.state.nlp_processor
    nlp_results = nlp_model.process_transcript(text)
    return nlp_results