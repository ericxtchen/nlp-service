from contextlib import asynccontextmanager
import threading

from fastapi import FastAPI
from .nlp_processor import NlpProcessor

from faststream.kafka import KafkaBroker
from faststream import FastStream
import httpx

nlp = NlpProcessor()

broker = KafkaBroker("localhost:9092")
stream_app = FastStream(broker)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as client:
        app.state.http_client = client
        yield

api_app = FastAPI(
    title="AI Scrum Bot - NLP Service",
    description="A microservice for processing meeting transcripts.",
    version="1.0.0",
    lifespan=lifespan
)

@api_app.get("/", tags=["Health Check"])
async def root():
    """
    Root endpoint for basic health check.
    """
    return {"status": "ok", "service": "NLP Processor"}