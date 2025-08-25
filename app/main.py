from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.api.routes import router as api_router
from app.events.router import router as kafka_router

# The primary FastAPI application is the single source of truth
app = FastAPI(
    title="Meeting Transcript NLP Processor",
    description="Microservice for processing meeting transcripts with NLP",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(kafka_router)
# Include your standard API routes
app.include_router(api_router)