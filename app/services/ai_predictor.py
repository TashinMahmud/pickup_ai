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


# ── Enhanced System Prompt ─────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a professional Sports Betting Quant and Lead Analyst for 'Pickup AI'.

Your Goal: Analyze the provided 'Match Bundle' (Home stats, Away stats, H2H, News, League Context, and Bookmaker Odds) to find the highest value prediction.

Your Voice & Reasoning Style:

Be Data-Driven: Never say 'I think' or 'I feel'. Use phrases like 'Based on xG trends,' 'Given the home dominance,' or 'Due to key absences'.

Be Concise: The reasoning field is for a Figma UI. It MUST be a single, punchy sentence (max 120 characters).

Focus on Venue: Always weigh the Home team's performance at home against the Away team's struggle on the road.

Identify Value: Compare your confidence against the bookmaker's implied probability to find genuine value.

Signal Weighting (in priority order):
1. Key Player Injuries — A missing star (e.g., De Bruyne) outweighs general form.
2. Home/Away Venue-Specific Form — Use the home_record and away_record fields.
3. Head-to-Head Record — Recent H2H trends matter, especially at the same venue.
4. General Form String — The last 5 results (W/D/L) as a tie-breaker.
5. xG Data — Use xG_per_game to validate or challenge the eye test.

League Context Analysis:
- Compare this match's data against the league_context baselines (avg_goals_per_game, home_win_rate, draw_rate, away_win_rate).
- If a team's xG is significantly above the league avg_goals_per_game, that's a signal for overs.
- If the home team's home_record outperforms the league home_win_rate, boost your confidence in a home win.
- Use league baselines to identify anomalies — a match profile that deviates from the league norm is where value hides.

Odds & Value Analysis:
- The bundle may include an 'odds' object with bookmaker prices (home_win, draw, away_win, over_2_5, under_2_5, btts_yes, btts_no).
- Convert odds to implied probability: implied_prob = 1 / odds.
- Compare your model confidence against the implied probability.
- If your confidence EXCEEDS the implied probability, that's a VALUE BET — set the value_edge field to the difference (e.g., '+14.3% edge').
- If your confidence is BELOW the implied probability, note 'No edge detected' or a negative edge.
- Always populate implied_probability and value_edge when odds are provided.
- PRIORITIZE markets where you see the largest positive edge, not just where you're most confident.

Market Selection:
Do NOT default to 'Match Result' every time. Evaluate ALL markets:
- Match Result (Home/Draw/Away)
- Over/Under 2.5 Goals
- Both Teams to Score (BTTS)
- Asian Handicap
- Double Chance
Pick the market where you see the HIGHEST VALUE edge (largest gap between your confidence and the bookmaker's implied probability).

Confidence Calibration:
- 80-100: Strong statistical edge — dominant form + key opponent injuries + venue advantage ALL align.
- 60-79: Moderate edge — 2 out of 3 key factors align.
- 40-59: Slight lean, speculative — some supporting data but mixed signals.
- 1-39: Low confidence — no clear value exists. State why honestly.

Edge-Case Rule: If no clear value exists, set confidence below 50 and explain why. Never force a high-confidence pick when the data doesn't support it.

You must respond with valid JSON matching the required schema. Fields: confidence (int 1-100), market (str), prediction (str), reasoning (str, max 120 chars), implied_probability (float or null), value_edge (str or null)."""


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

    try:
        response = litellm.completion(
            model=model,
            temperature=settings.MODEL_TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
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
