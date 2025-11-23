from pydantic import BaseModel
from typing import Optional, Dict, Any


class ScoreRequest(BaseModel):
    transcript: str
    duration_seconds: Optional[float] = None


class ScoreResponse(BaseModel):
    overall_score: float
    criteria_scores: Dict[str, Dict[str, Any]]
    word_count: int
    sentence_count: int
