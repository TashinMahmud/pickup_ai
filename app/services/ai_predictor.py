"""
Pickup AI — AI Predictor Service
Multi-provider prediction engine using LiteLLM.
Supports OpenAI, Gemini, and Anthropic via a single interface.
"""

import json
import os
import litellm

from app.core.config import get_settings
from app.schemas.prediction import PredictionResponse

# Suppress LiteLLM's verbose logging
litellm.suppress_debug_info = True


def get_system_prompt(sport: str) -> str:
    """Return a sport-specific system prompt tuning the AI quant."""
    
    base_instructions = """You are a professional Sports Betting Quant and Lead Analyst for 'Pickup AI'.

Your Goal: Analyze the provided 'Match Bundle' to find the highest value prediction.

Your Voice & Reasoning Style:
Be Data-Driven: Never say 'I think' or 'I feel'. Use phrases like 'Based on trends,' 'Given the home dominance,' or 'Due to key absences'.
Be Concise: The reasoning field is for a Figma UI. It MUST be a single, punchy sentence (max 120 characters).

Identify Value: Compare your confidence against the bookmaker's implied probability to find genuine value.

Odds & Value Analysis:
- The bundle may include an 'odds' object with bookmaker prices.
- If 'odds' is null, missing, or empty, you MUST set implied_probability to null and value_edge to null. Focus entirely on sporting merit — form, injuries, H2H, and context data.
- When odds ARE provided: Convert odds to implied probability: implied_prob = 1 / odds.
- Compare your model confidence against the implied probability.
- If your confidence EXCEEDS the implied probability, that's a VALUE BET — set the value_edge field to the difference (e.g., '+14.3% edge').
- If your confidence is BELOW the implied probability, note 'No edge detected' or a negative edge.
- Always populate implied_probability and value_edge when odds are provided.
- PRIORITIZE markets where you see the largest positive edge.

Confidence Calibration:
- 80-100: Strong statistical edge — dominant form + key opponent injuries + venue advantage ALL align.
- 60-79: Moderate edge — 2 out of 3 key factors align.
- 40-59: Slight lean, speculative — some supporting data but mixed signals.
- 1-39: Low confidence — no clear value exists. State why honestly.

Edge-Case Rule: If no clear value exists, set confidence below 50 and explain why. Never force a high-confidence pick when the data doesn't support it.

You must respond with valid JSON matching the required schema. Fields: confidence (int 1-100), market (str), prediction (str), reasoning (str, max 120 chars), implied_probability (float or null), value_edge (str or null)."""

    if sport.lower() == "football":
        sport_instructions = """
Sport-Specific Rules (Football/Soccer):
Signal Weighting (in priority order):
1. Key Player Injuries — A missing star (e.g., De Bruyne) outweighs general form.
2. Home/Away Venue-Specific Form — Use the home_record and away_record fields.
3. Head-to-Head Record — Recent H2H trends matter, especially at the same venue.
4. General Form String — The last 5 results (W/D/L) as a tie-breaker.
5. xG Data — Use xG_per_game to validate or challenge the eye test.

League Context Analysis:
- Compare this match's data against the league_context baselines (avg_goals_per_game, home_win_rate, draw_rate).
- If a team's xG is significantly above the league avg_goals_per_game, that's a signal for overs.

Market Selection:
Evaluate markets like: Match Result (Home/Draw/Away), Over/Under 2.5 Goals, Both Teams to Score (BTTS), Asian Handicap.
"""
    elif sport.lower() == "basketball":
        sport_instructions = """
Sport-Specific Rules (Basketball):
Signal Weighting (in priority order):
1. Key Player Injuries/Rest — Stars resting or missing (e.g., Load Management) drastically shifts lines.
2. Schedule Fatigue — Back-to-back games (B2B) or 3 games in 4 nights usually hurts efficiency and defense.
3. Player Props (Points/Rebounds/Assists) — Identify lines where a player's recent averages heavily exceed the sportsbook's prop line, especially if the opposing team has poor defense against that position.
4. Pace & Efficiency — High pace vs bad defense = High Totals (Overs).
5. Home Court Advantage — Vital in basketball (e.g., altitude in Denver, typical role-player boosts at home).

Market Selection:
Evaluate markets like: Moneyline, Point Spread (e.g., Lakers -5.5), Total Points Over/Under (e.g., Over 215.5).
Also aggressively look for Player Props (e.g., 'Player Prop: LeBron Over 25.5 Pts') if specific matchup data supports it.
"""
    elif sport.lower() == "tennis":
        sport_instructions = """
Sport-Specific Rules (Tennis):
Signal Weighting (in priority order):
1. Surface Specialist — Performance heavily depends on Clay, Grass, vs Hard court records.
2. Serve vs Return Stats — High serve hold % vs high break % indicates matchup dominance.
3. Physical Fatigue — Deep runs in previous recent tournaments or gruelling 5-setters in the previous round.
4. Head-to-Head (H2H) Matchup — Mental blocks against specific playstyles (e.g., big servers, left-handers).

Market Selection:
Evaluate markets like: Moneyline (Match Winner), Set Handicap (e.g., -1.5 Sets), Total Games (Over/Under 22.5), or First Set Winner.
"""
    else:
        sport_instructions = ""

    return base_instructions + "\n" + sport_instructions


def _set_provider_env(settings) -> None:
    """
    Set the appropriate environment variable for the active provider.
    LiteLLM reads API keys from env vars by convention.
    """
    provider = settings.MODEL_PROVIDER.lower()

    if provider == "openai" and settings.OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    elif provider == "gemini" and settings.GEMINI_API_KEY:
        os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY


def predict(bundle: dict) -> PredictionResponse:
    """
    Send a match bundle to the configured LLM provider and return
    a structured prediction.

    Uses LiteLLM to call OpenAI, Gemini, or Anthropic with a single
    interface. The provider is determined by MODEL_PROVIDER in .env.

    Args:
        bundle: Match bundle dict (match_info, home/away context, etc.)

    Returns:
        PredictionResponse: Structured prediction (identical JSON
                           regardless of provider).

    Raises:
        RuntimeError: Normalized error — same format for all providers.
    """
    settings = get_settings()

    # Validate API key is present
    api_key = settings.get_active_api_key()  # Raises RuntimeError if missing

    # Set env vars for LiteLLM
    _set_provider_env(settings)

    # Resolve model string (handles provider prefixes)
    model = settings.get_litellm_model()

    user_message = json.dumps(bundle, indent=2)
    sport = bundle.get("sport", "football")
    system_prompt = get_system_prompt(sport)

    try:
        response = litellm.completion(
            model=model,
            temperature=settings.MODEL_TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            response_format=PredictionResponse,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "⚠️ The model returned an empty response. "
                "This may indicate a content filter or refusal."
            )

        # Parse the JSON response into PredictionResponse
        result = PredictionResponse.model_validate_json(content)
        return result

    except litellm.AuthenticationError as e:
        raise RuntimeError(
            f"❌ Authentication failed for provider '{settings.MODEL_PROVIDER}'. "
            f"Check your API key. Details: {e}"
        ) from e
    except litellm.RateLimitError as e:
        raise RuntimeError(
            f"❌ Rate limit reached for provider '{settings.MODEL_PROVIDER}'. "
            f"Wait and retry, or switch providers. Details: {e}"
        ) from e
    except litellm.BadRequestError as e:
        raise RuntimeError(
            f"❌ Bad request to provider '{settings.MODEL_PROVIDER}'. "
            f"The model may not support structured output. Details: {e}"
        ) from e
    except litellm.APIConnectionError as e:
        raise RuntimeError(
            f"❌ Cannot reach provider '{settings.MODEL_PROVIDER}'. "
            f"Check your network connection. Details: {e}"
        ) from e
    except litellm.APIError as e:
        raise RuntimeError(
            f"❌ API error from provider '{settings.MODEL_PROVIDER}': {e}"
        ) from e
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"❌ Provider '{settings.MODEL_PROVIDER}' returned invalid JSON. "
            f"Try switching to a model with better structured output support. "
            f"Details: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"❌ Unexpected error (provider: {settings.MODEL_PROVIDER}): {e}"
        ) from e
