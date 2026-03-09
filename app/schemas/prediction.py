"""
Pickup AI — Prediction Schema
Pydantic model for structured AI output.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PredictionResponse(BaseModel):
    """Structured prediction output from the AI predictor."""

    confidence: int = Field(
        ge=1,
        le=100,
        description=(
            "Confidence level 1-100. "
            "80-100 = strong statistical edge, "
            "60-79 = moderate edge, "
            "40-59 = slight lean / speculative, "
            "1-39 = low confidence / no clear value."
        ),
    )
    market: str = Field(
        description=(
            "The betting market with the highest value. "
            "Examples: 'Match Result', 'Moneyline', 'Point Spread -5.5', "
            "'Player Prop: LeBron Over 25.5 Pts', 'Over/Under 215.5', "
            "'Set Handicap -1.5'."
        ),
    )
    prediction: str = Field(
        description=(
            "The specific pick within the chosen market. "
            "Examples: 'Arsenal Win', 'Lakers -5.5', 'Djokovic 3-0'."
        ),
    )
    reasoning: str = Field(
        max_length=120,
        description=(
            "A single, punchy sentence explaining the pick. "
            "Must be data-driven and max 120 characters. "
            "Designed to fit a Figma UI card."
        ),
    )
    implied_probability: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description=(
            "The implied probability from the bookmaker odds for the chosen market. "
            "Calculated as 1/odds. Example: odds 2.10 → 0.476."
        ),
    )
    value_edge: Optional[str] = Field(
        default=None,
        description=(
            "The value edge percentage if odds are provided. "
            "Positive = value bet, Negative = overpriced. "
            "Example: '+14.3% edge' or 'No edge detected'."
        ),
    )
