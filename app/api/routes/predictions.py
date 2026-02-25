"""
Pickup AI — Prediction API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.schemas.prediction import PredictionResponse
from app.services.ai_predictor import predict

router = APIRouter(prefix="/api", tags=["predictions"])


# ── Request Schema ─────────────────────────────────────────────────────────────


class MatchBundle(BaseModel):
    """Request body for the /predict endpoint."""

    match_info: dict
    home_team_context: dict
    away_team_context: dict
    h2h_context: str
    news_context: Optional[str] = None
    league_context: Optional[dict] = None
    odds: Optional[dict] = None


# ── Routes ─────────────────────────────────────────────────────────────────────


@router.post("/predict", response_model=PredictionResponse)
async def predict_match(bundle: MatchBundle):
    """
    Accept a match bundle and return an AI-generated prediction.

    The AI analyzes the home/away context, H2H record, and news
    to find the highest-value betting market prediction.
    """
    try:
        result = predict(bundle.model_dump())
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
