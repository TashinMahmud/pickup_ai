"""Quick test script to debug the /predict endpoint."""
import urllib.request
import json

bundle = {
    "match_info": {"home": "Arsenal", "away": "Man City", "date": "2026-03-01"},
    "home_team_context": {
        "form": "W-W-W-D-L",
        "avg_goals": 2.1,
        "injuries": ["Odegaard (Questionable)"],
        "home_record": "W8-D2-L1",
        "xG_per_game": 2.3,
    },
    "away_team_context": {
        "form": "W-L-W-W-W",
        "avg_goals": 1.9,
        "injuries": ["De Bruyne (Out)"],
        "away_record": "W5-D3-L3",
        "xG_per_game": 1.7,
    },
    "h2h_context": "City won 4 of 5, Arsenal won most recent home 1-0.",
    "odds": {"home_win": 2.10, "draw": 3.40, "away_win": 3.60},
}

req = urllib.request.Request(
    "http://localhost:8000/api/predict",
    data=json.dumps(bundle).encode(),
    headers={"Content-Type": "application/json"},
)

try:
    r = urllib.request.urlopen(req)
    print("SUCCESS:")
    print(json.dumps(json.loads(r.read()), indent=2))
except urllib.error.HTTPError as e:
    print(f"ERROR {e.code}:")
    print(e.read().decode())
except Exception as e:
    print(f"CONNECTION ERROR: {e}")
