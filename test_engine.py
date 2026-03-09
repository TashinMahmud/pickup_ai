"""
Pickup AI — Test Engine
Runs the AI predictor against 3 different match bundles and prints results.
"""

import json
import sys

from app.data.data_simulator import get_match_bundles
from app.services.ai_predictor import predict


# ── ANSI Colors ────────────────────────────────────────────────────────────────

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


# ── Bundle Labels ──────────────────────────────────────────────────────────────

BUNDLE_LABELS = {
    "football": "⚽ Football",
    "basketball": "🏀 Basketball",
    "tennis": "🎾 Tennis",
}

def print_separator():
    print(f"{DIM}{'━' * 60}{RESET}")


def print_bundle_header(sport: str, match_info: dict, league_context: dict = None):
    label = BUNDLE_LABELS.get(sport, sport.capitalize())
    home = match_info.get("home") or match_info.get("player_1", "Unknown")
    away = match_info.get("away") or match_info.get("player_2", "Unknown")
    date = match_info["date"]
    print()
    print_separator()
    print(f"{BOLD}{CYAN}{label}: {home} vs {away}{RESET}")
    print(f"{DIM}  📅 {date}{RESET}")
    if league_context:
        league = league_context.get("league", "Unknown")
        print(f"{DIM}  🏆 {league}{RESET}")
    print_separator()


def print_odds(odds: dict):
    """Print the configured bookmaker odds."""
    odds_str = " | ".join([f"{k} {v}" for k, v in odds.items()])
    print(f"  {DIM}📊 Odds: {odds_str}{RESET}")


def print_prediction(prediction):
    """Pretty-print a PredictionResponse."""
    data = prediction.model_dump()

    # Color confidence based on level
    conf = data["confidence"]
    if conf >= 80:
        conf_color = GREEN
    elif conf >= 60:
        conf_color = YELLOW
    else:
        conf_color = RED

    print(f"  {BOLD}Market:{RESET}      {data['market']}")
    print(f"  {BOLD}Prediction:{RESET}  {data['prediction']}")
    print(f"  {BOLD}Confidence:{RESET}  {conf_color}{conf}%{RESET}")
    print(f"  {BOLD}Reasoning:{RESET}   {data['reasoning']}")

    # Show value analysis if available
    if data.get("implied_probability") is not None:
        imp_prob = data["implied_probability"]
        print(f"  {BOLD}Implied Prob:{RESET} {MAGENTA}{imp_prob:.1%}{RESET}")
    if data.get("value_edge"):
        edge = data["value_edge"]
        edge_color = GREEN if "+" in edge else RED
        print(f"  {BOLD}Value Edge:{RESET}  {edge_color}{edge}{RESET}")

    print()
    print(f"  {DIM}Raw JSON:{RESET}")
    print(f"  {json.dumps(data, indent=2)}")
    print()


def main():
    bundles = get_match_bundles()

    print()
    print(f"{BOLD}{CYAN}+----------------------------------------------------------+{RESET}")
    print(f"{BOLD}{CYAN}|          🏈  PICKUP AI — PREDICTION ENGINE  🏈          |{RESET}")
    print(f"{BOLD}{CYAN}+----------------------------------------------------------+{RESET}")
    print()

    for bundle in bundles:
        sport = bundle.get("sport", "football")

        print_bundle_header(
            sport,
            bundle["match_info"],
            bundle.get("league_context"),
        )

        # Show odds if available
        if bundle.get("odds"):
            print_odds(bundle["odds"])
            print()

        try:
            prediction = predict(bundle)
            print_prediction(prediction)
        except RuntimeError as e:
            print(f"  {RED}{e}{RESET}")
            print()

    print_separator()
    print(f"{BOLD}{GREEN}✅ All {len(bundles)} bundles processed.{RESET}")
    print()


if __name__ == "__main__":
    main()
