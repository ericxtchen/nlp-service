from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
import logging

logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as client:
        logger.info("Starting Microservice Application")
        app.state.http_client = client
        logger.info("Application Startup Complete")
        yield 
        logger.info("Shutting down Microservice Application")
        logger.info("Microservice Application Shut Down")
        