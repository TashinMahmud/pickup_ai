"""
Pickup AI — Data Simulator
Generates realistic match bundles for the AI prediction engine.
"""


def get_match_bundles() -> list[dict]:
    """
    Returns 3 match bundles representing different match archetypes:
    1. Top-table clash
    2. Relegation battle
    3. Mid-table game

    Each bundle includes league context and bookmaker odds.
    """

    bundles = [
        # ── Bundle 1: Top-Table Clash ──────────────────────────────────
        {
            "match_info": {
                "home": "Arsenal",
                "away": "Man City",
                "date": "2026-03-01",
            },
            "league_context": {
                "league": "Premier League",
                "season": "2025-26",
                "avg_goals_per_game": 2.77,
                "home_win_rate": 0.46,
                "draw_rate": 0.24,
                "away_win_rate": 0.30,
            },
            "home_team_context": {
                "form": "W-W-W-D-L",
                "avg_goals": 2.1,
                "injuries": ["Odegaard (Questionable)"],
                "home_record": "W8-D2-L1 at Emirates this season",
                "xG_per_game": 2.3,
            },
            "away_team_context": {
                "form": "W-L-W-W-W",
                "avg_goals": 1.9,
                "injuries": ["De Bruyne (Out)"],
                "away_record": "W5-D3-L3 on the road this season",
                "xG_per_game": 1.7,
            },
            "odds": {
                "home_win": 2.10,
                "draw": 3.40,
                "away_win": 3.60,
                "over_2_5": 1.85,
                "under_2_5": 2.00,
                "btts_yes": 1.75,
                "btts_no": 2.10,
            },
            "h2h_context": (
                "Man City has won 4 of the last 5 meetings, "
                "but Arsenal won the most recent home game 1-0."
            ),
            "news_context": (
                "Arteta confirmed a 4-3-3 formation in his pre-match press "
                "conference. Saka is fully fit and expected to start."
            ),
        },
        # ── Bundle 2: Relegation Battle ────────────────────────────────
        {
            "match_info": {
                "home": "Burnley",
                "away": "Sheffield United",
                "date": "2026-03-01",
            },
            "league_context": {
                "league": "Premier League",
                "season": "2025-26",
                "avg_goals_per_game": 2.77,
                "home_win_rate": 0.46,
                "draw_rate": 0.24,
                "away_win_rate": 0.30,
            },
            "home_team_context": {
                "form": "L-D-L-L-W",
                "avg_goals": 0.8,
                "injuries": ["Rodriguez (Doubtful)", "Cork (Out)"],
                "home_record": "W2-D4-L5 at Turf Moor this season",
                "xG_per_game": 0.9,
            },
            "away_team_context": {
                "form": "L-L-D-L-L",
                "avg_goals": 0.5,
                "injuries": ["Brewster (Out)", "McBurnie (Doubtful)"],
                "away_record": "W1-D2-L8 on the road this season",
                "xG_per_game": 0.6,
            },
            "odds": {
                "home_win": 2.25,
                "draw": 3.10,
                "away_win": 3.50,
                "over_2_5": 3.20,
                "under_2_5": 1.36,
                "btts_yes": 2.80,
                "btts_no": 1.45,
            },
            "h2h_context": (
                "Last 4 meetings have produced only 3 total goals. "
                "Burnley won the reverse fixture 1-0 with a late set-piece goal."
            ),
            "news_context": (
                "Sheffield United manager confirmed they will prioritize "
                "defensive solidity. Burnley's new signing Benson is available."
            ),
        },
        # ── Bundle 3: Mid-Table Game ───────────────────────────────────
        {
            "match_info": {
                "home": "Wolves",
                "away": "Bournemouth",
                "date": "2026-03-02",
            },
            "league_context": {
                "league": "Premier League",
                "season": "2025-26",
                "avg_goals_per_game": 2.77,
                "home_win_rate": 0.46,
                "draw_rate": 0.24,
                "away_win_rate": 0.30,
            },
            "home_team_context": {
                "form": "W-L-W-D-D",
                "avg_goals": 1.3,
                "injuries": ["Kalajdzic (Out)"],
                "home_record": "W4-D3-L4 at Molineux this season",
                "xG_per_game": 1.4,
            },
            "away_team_context": {
                "form": "D-W-L-W-D",
                "avg_goals": 1.5,
                "injuries": [],
                "away_record": "W3-D4-L4 on the road this season",
                "xG_per_game": 1.3,
            },
            "odds": {
                "home_win": 2.50,
                "draw": 3.25,
                "away_win": 2.90,
                "over_2_5": 1.95,
                "under_2_5": 1.90,
                "btts_yes": 1.65,
                "btts_no": 2.25,
            },
            "h2h_context": (
                "The last 3 meetings between these sides have all ended in draws. "
                "Both teams scored in 4 of the last 5 encounters."
            ),
            "news_context": (
                "Bournemouth have a fully fit squad for the first time this "
                "season. Wolves' Cunha is in red-hot form with 5 goals in 4 games."
            ),
        },
    ]

    return bundles
