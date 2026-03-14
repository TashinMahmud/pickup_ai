import json
import time

# ANSI color codes for pretty terminal output
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ── 1. The Fake Database (Mock JSON Payloads) ──────────────────────────────────
# These represent exactly what the backend team would send as JSON.

MOCK_DATABASE = [
    # ── FOOTBALL SCENARIOS ───────────────────────────────────────────────────
    # Scenario 1: Exact payload from backend team (Hibernian vs Livingston)
    {
        "success": None,
        "message": None,
        "data": {
            "sport": "football",
            "match_info": {"home": "Hibernian", "away": "Livingston", "date": "2026-03-14 15:00:00"},
            "league_context": {"league": "2025/2026", "season": "2025/2026", "avg_goals_per_game": 0, "home_win_rate": 0, "draw_rate": 0, "away_win_rate": 0},
            "home_team_context": {"form": "D-W-W-L-W", "avg_goals": 2, "injuries": [], "home_record": "W7-D5-L2 at home this season", "xG_per_game": 0},
            "away_team_context": {"form": "D-D-D-L-L", "avg_goals": 1.4, "injuries": [], "away_record": "W0-D5-L9 on the road this season", "xG_per_game": 0},
            "odds": None,
            "h2h_context": "Hibernian has won 3 of the last 5 meetings. The most recent match ended 2-2.",
            "news_context": "Team news and lineups are updated in real-time. Saka and Odegaard are monitored."
        }
    },
    # Scenario 2: Football with odds present
    {
        "success": True,
        "message": "AI analysis data retrieved",
        "data": {
            "sport": "football",
            "match_info": {"home": "Arsenal", "away": "Man City", "date": "2026-03-01"},
            "league_context": {"league": "Premier League", "avg_goals_per_game": 2.77},
            "home_team_context": {"form": "W-W-W-D-L", "avg_goals": 2.1, "injuries": ["Odegaard (Questionable)"]},
            "away_team_context": {"form": "W-L-W-W-W", "avg_goals": 1.9, "injuries": ["De Bruyne (Out)"]},
            "odds": {"home_win": 2.10, "draw": 3.40, "away_win": 3.60, "over_2_5": 1.85},
            "h2h_context": "Man City won 4 of last 5, but Arsenal won the most recent home game 1-0."
        }
    },

    # ── BASKETBALL SCENARIOS ─────────────────────────────────────────────────
    # Scenario 3: Basketball with odds
    {
        "success": True,
        "message": "AI analysis data retrieved",
        "data": {
            "sport": "basketball",
            "match_info": {"home": "Lakers", "away": "Nuggets", "date": "2026-03-02"},
            "home_team_context": {"form": "W-L-W-W-L", "injuries": ["Davis (Probable)"], "pace": 102.3},
            "away_team_context": {"form": "W-W-W-W-L", "injuries": ["Murray (Out - Rest)"], "pace": 98.5},
            "odds": {"home_win_moneyline": 2.05, "away_win_moneyline": 1.76, "over_225_5": 1.90, "LeBron_Over_25_5_pts": 1.85},
            "h2h_context": "Denver is on the second night of a back-to-back."
        }
    },
    # Scenario 4: Basketball with null odds
    {
        "success": True,
        "message": None,
        "data": {
            "sport": "basketball",
            "match_info": {"home": "Celtics", "away": "Pistons", "date": "2026-03-12"},
            "home_team_context": {"form": "W-W-W-W-W", "home_record": "28-1 at home"},
            "away_team_context": {"form": "L-L-L-L-L", "away_record": "4-25 on road"},
            "odds": None,
            "h2h_context": "Celtics beat them by 30 points last time."
        }
    },

    # ── TENNIS SCENARIOS ─────────────────────────────────────────────────────
    # Scenario 5: Exact payload from backend team (Sanchez vs Rocha)
    {
        "success": True,
        "data": {
            "sport": "tennis",
            "match_info": {"home": "N. Sanchez Izquierdo", "away": "H. Rocha", "date": "2026-03-13"},
            "league_context": {"league": "Santiago", "surface": "Hard Court"},
            "home_team_context": {"form": "W-L-W-W-W", "injuries": ["Unknown"], "serve_hold_percentage": 78.3, "current_rank": 0, "current_points": 0, "recent_performance": "8 wins in last 15 matches", "avg_aces_per_match": 1.2},
            "away_team_context": {"form": "W-L-L-L-W", "injuries": ["Unknown"], "serve_hold_percentage": 82.9, "current_rank": 0, "current_points": 0, "recent_performance": "10 wins in last 14 matches", "avg_aces_per_match": 3.2},
            "odds": None,
            "h2h_context": "N. Sanchez Izquierdo leads 0-1 overall. Last match: 1 - 2. Total meetings: 1."
        },
        "message": "AI analysis data retrieved"
    },
    # Scenario 6: Tennis with odds
    {
        "success": True,
        "message": "AI analysis data retrieved",
        "data": {
            "sport": "tennis",
            "match_info": {"home": "Alcaraz", "away": "Medvedev", "date": "2026-03-08"},
            "league_context": {"league": "Wimbledon", "surface": "Grass Court"},
            "home_team_context": {"form": "W-W-W-W-W", "serve_hold_percentage": 92.1, "recent_performance": "14 wins in last 15 matches"},
            "away_team_context": {"form": "W-W-L-W-L", "serve_hold_percentage": 85.0, "recent_performance": "Medvedev hates grass courts."},
            "odds": {"player_1_win": 1.45, "player_2_win": 2.80},
            "h2h_context": "Alcaraz dominated Medvedev at Wimbledon last year."
        }
    }
]


# ── 2. The Simulation Runner ───────────────────────────────────────────────────

def run_scenarios():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{MAGENTA}            PICKUP AI - VISUAL SCENARIO TESTING TERMINAL              {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}\n")
    print(f"This script simulates what happens when your backend sends JSON to the AI.\n")
    
    # We import the internal predictor directly to avoid needing the web server running
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from app.services.ai_predictor import predict

    for index, payload in enumerate(MOCK_DATABASE, start=1):
        # Unpack the wrapper — the AI only needs the inner "data" object
        inner_data = payload.get("data", payload)
        sport = inner_data.get("sport", "unknown").upper()
        print(f"\n{BOLD}{CYAN}--- SCENARIO {index}: {sport} MATCH ---{RESET}")
        print("-" * 70)
        
        # 1. Show the INPUT (What the backend sends — full wrapper)
        print(f"{BOLD}1. [INPUT] BACKEND SENDS THIS JSON PAYLOAD TO `/api/predict`:{RESET}")
        print(f"{CYAN}{json.dumps(payload, indent=2)}{RESET}")
        
        print(f"\n{YELLOW}      [ Pickup AI is processing... ]{RESET}")
        time.sleep(1) # Dramatic pause for effect

        # 2. Process via AI Model (pass only the inner data)
        try:
            result = predict(inner_data)
            
            # The result is a Pydantic object, we convert it to dict for printing
            final_output_json = result.model_dump()
            
            # 3. Show the OUTPUT (What the backend receives)
            print(f"\n{BOLD}2. [OUTPUT] PICKUP AI OUTPUTS THIS JSON RESPONSE & SAVES TO POSTGRES:{RESET}")
            print(f"{GREEN}{json.dumps(final_output_json, indent=2)}{RESET}\n")

        except Exception as e:
            print(f"\n{BOLD}[ERROR] OCCURRED (Likely missing API Key or limit reached):{RESET} {e}\n")
            
        print(f"{BOLD}{MAGENTA}======================================================================{RESET}")

if __name__ == "__main__":
    run_scenarios()
