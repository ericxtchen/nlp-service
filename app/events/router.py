from faststream.kafka.fastapi import KafkaRouter
from app.services.transcript import fetch_transcript, process_transcript, transcript_to_text
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = KafkaRouter(settings.KAFKA_BOOTSTRAP)

@router.subscriber("transcripts-to-process")
@router.publisher("processed-transcripts")
async def process_message(msg: str):
    try:
        logger.info(f"Received bot ID message: {msg}")
        from main import app
        client = app.state.http_client
        transcript_data = await fetch_transcript(msg, client)
        text = transcript_to_text(transcript_data)
        nlp_results = process_transcript(text)
        logger.info(f"Processed transcript for bot_id: {msg}")
        return nlp_results
    except Exception as e:
        logger.error(f"Error processing bot_id {msg}: {str(e)}")
        raise