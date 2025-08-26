from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Timestamp(BaseModel):
    absolute: float  # seconds
    relative: float  # seconds


class Word(BaseModel):
    text: str
    start_timestamp: Timestamp
    end_timestamp: Timestamp


class Participant(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class TranscriptEntry(BaseModel):
    participant: Participant
    words: List[Word]


class Transcript(BaseModel):
    entries: List[TranscriptEntry]
