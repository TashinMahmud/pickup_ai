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
        # ── Bundle 1: Football (Top-Table Clash) ───────────────────────
        {
            "sport": "football",
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
        # ── Bundle 2: Basketball (Western Conference) ──────────────────
        {
            "sport": "basketball",
            "match_info": {
                "home": "Lakers",
                "away": "Nuggets",
                "date": "2026-03-02",
            },
            "league_context": {
                "league": "NBA",
                "season": "2025-26",
                "avg_points_per_game": 228.5,
                "home_win_rate": 0.58,
            },
            "home_team_context": {
                "form": "W-L-W-W-L",
                "avg_points_scored": 114.2,
                "avg_points_allowed": 112.5,
                "injuries": ["Davis (Probable)"],
                "home_record": "W12-L4 at Crypto.com this season",
                "pace": 102.3,
                "offensive_rating": 115.1,
                "defensive_rating": 113.8,
                "key_player_averages": {
                    "LeBron_James": {"pts": 24.5, "ast": 8.1, "reb": 7.5}
                }
            },
            "away_team_context": {
                "form": "W-W-W-W-L",
                "avg_points_scored": 116.8,
                "avg_points_allowed": 110.1,
                "injuries": ["Murray (Out - Rest)"],
                "away_record": "W9-L7 on the road this season",
                "pace": 98.5,
                "offensive_rating": 118.5,
                "defensive_rating": 110.2,
                "key_player_averages": {
                    "Nikola_Jokic": {"pts": 26.2, "ast": 9.5, "reb": 12.1}
                }
            },
            "odds": {
                "home_win_moneyline": 2.05,
                "away_win_moneyline": 1.76,
                "home_spread_plus_2_5": 1.90,
                "away_spread_minus_2_5": 1.90,
                "over_225_5": 1.90,
                "under_225_5": 1.90,
                "LeBron_Over_25_5_pts": 1.85,
                "Jokic_Over_10_5_ast": 1.70,
            },
            "h2h_context": (
                "Denver has won 8 of the last 10 matchups, including playoffs. "
                "Lakers struggle against Jokic's passing out of double teams."
            ),
            "news_context": (
                "Denver is on the second night of a back-to-back (B2B) and resting Jamal Murray. "
                "Lakers have had 3 days of rest."
            ),
        },
        # ── Bundle 3: Tennis (Grand Slam Semi-Final) ───────────────────
        {
            "sport": "tennis",
            "match_info": {
                "player_1": "Sinner",
                "player_2": "Djokovic",
                "date": "2026-03-03",
                "tournament": "Australian Open (Hard Court)",
                "round": "Semi-Final",
            },
            "home_team_context": {
                "name": "Jannik Sinner",
                "form_last_5": "W-W-W-W-W",
                "serve_hold_pct": "91%",
                "return_break_pct": "28%",
                "injuries": [],
                "recent_fatigue": "Won previous round in straight sets (2h 10m).",
                "hard_court_win_rate": "82%",
            },
            "away_team_context": {
                "name": "Novak Djokovic",
                "form_last_5": "W-W-W-W-W",
                "serve_hold_pct": "89%",
                "return_break_pct": "31%",
                "injuries": ["Right Wrist (Taped - Minor)"],
                "recent_fatigue": "Survived a 5-set thriller in QF (4h 15m).",
                "hard_court_win_rate": "88%",
            },
            "odds": {
                "player_1_win": 1.80,
                "player_2_win": 2.05,
                "over_39_5_games": 1.90,
                "under_39_5_games": 1.90,
                "player_1_minus_1_5_sets": 2.30,
            },
            "h2h_context": (
                "H2H is tied 3-3. Sinner has won the last two meetings on Hard Courts, "
                "including their previous clash at this exact tournament last year."
            ),
            "news_context": "Djokovic appeared physically exhausted in the QF post-match press conference.",
            "league_context": None, # Tennis doesn't map perfectly to league_context
        },
    ]

    return bundles

    return bundles
