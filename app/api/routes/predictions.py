"""
Pickup AI — Prediction API Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.prediction import PredictionResponse
from app.services.ai_predictor import predict
from app.core.database import get_db
from app.model.prediction import Prediction

router = APIRouter(prefix="/api", tags=["predictions"])


# ── Request Schema ─────────────────────────────────────────────────────────────


class MatchBundle(BaseModel):
    """Request body for the /predict endpoint."""

    sport: str = "football"
    match_info: dict
    home_team_context: dict
    away_team_context: dict
    h2h_context: str
    news_context: Optional[str] = None
    league_context: Optional[dict] = None
    odds: Optional[dict] = None


# ── Helpers ────────────────────────────────────────────────────────────────────


def _generate_match_id(sport: str, match_info: dict) -> str:
    """Generate a unique match_id from match_info fields."""
    home = match_info.get("home") or match_info.get("player_1", "unknown")
    home = home.replace(" ", "_").lower()
    away = match_info.get("away") or match_info.get("player_2", "unknown")
    away = away.replace(" ", "_").lower()
    date = match_info.get("date", "unknown")
    return f"{sport}_{home}_vs_{away}_{date}"


def _save_prediction(
    db: Session,
    match_id: str,
    result: PredictionResponse,
) -> Prediction:
    """
    Save or update a prediction in the database.
    Uses upsert logic — if match_id exists, update the row.
    """
    existing = db.query(Prediction).filter(Prediction.match_id == match_id).first()

    if existing:
        existing.confidence = result.confidence
        existing.market = result.market
        existing.prediction_value = result.prediction
        existing.reasoning = result.reasoning
        existing.value_edge = result.value_edge
        existing.implied_probability = result.implied_probability
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_prediction = Prediction(
            match_id=match_id,
            confidence=result.confidence,
            market=result.market,
            prediction_value=result.prediction,
            reasoning=result.reasoning,
            value_edge=result.value_edge,
            implied_probability=result.implied_probability,
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return db_prediction


# ── Routes ─────────────────────────────────────────────────────────────────────


@router.post("/predict", response_model=PredictionResponse)
async def predict_match(bundle: MatchBundle, db: Session = Depends(get_db)):
    """
    Accept a match bundle, generate an AI prediction, save it to the
    database, and return the JSON response.

    The prediction will automatically appear in the Postgres
    `predictions` table with a unique match_id.
    """
    try:
        result = predict(bundle.model_dump())
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save to database
    try:
        match_id = _generate_match_id(bundle.sport, bundle.match_info)
        _save_prediction(db, match_id, result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction generated but failed to save to database: {e}",
        )

    return result
