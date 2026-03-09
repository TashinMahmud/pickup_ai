"""
Pickup AI — Prediction Database Model
SQLAlchemy model for the predictions table.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime

from app.core.database import Base


class Prediction(Base):
    """Predictions table — stores every AI prediction made via the API."""

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(String, unique=True, nullable=False, index=True)
    confidence = Column(Integer, nullable=False)
    market = Column(String, nullable=False)
    prediction_value = Column(String, nullable=False)
    reasoning = Column(String(120), nullable=False)
    value_edge = Column(String, nullable=True)
    implied_probability = Column(Float, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return (
            f"<Prediction(match_id='{self.match_id}', "
            f"market='{self.market}', "
            f"prediction='{self.prediction_value}')>"
        )
