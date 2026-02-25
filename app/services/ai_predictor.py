"""
Pickup AI — AI Predictor Service
Uses OpenAI GPT-4o mini with Structured Outputs to generate predictions.
"""

import json
from openai import OpenAI, OpenAIError

from app.core.config import get_settings
from app.schemas.prediction import PredictionResponse


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

Constraint: You must ONLY output JSON matching the required schema. Do not include any conversational filler."""


def predict(bundle: dict) -> PredictionResponse:
    """
    Send a match bundle to GPT-4o mini and return a structured prediction.

    Args:
        bundle: A dictionary containing match_info, home_team_context,
                away_team_context, h2h_context, and optionally news_context,
                league_context, and odds.

    Returns:
        PredictionResponse: Structured prediction with confidence, market,
                           prediction, reasoning, implied_probability, and value_edge.

    Raises:
        RuntimeError: If the API call fails or returns an unparseable response.
    """
    settings = get_settings()

    if not settings.OPENAI_API_KEY:
        raise RuntimeError(
            "❌ OPENAI_API_KEY is not set. "
            "Add it to your .env file: OPENAI_API_KEY=sk-your-key-here"
        )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    user_message = json.dumps(bundle, indent=2)

    try:
        completion = client.beta.chat.completions.parse(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            response_format=PredictionResponse,
        )

        result = completion.choices[0].message.parsed

        if result is None:
            raise RuntimeError(
                "⚠️ The model returned a response that could not be parsed "
                "into the PredictionResponse schema. This may indicate a "
                "refusal or malformed output."
            )

        return result

    except OpenAIError as e:
        raise RuntimeError(f"❌ OpenAI API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"❌ Unexpected error during prediction: {e}") from e
