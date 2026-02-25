# Pickup AI

AI-powered sports betting prediction engine using OpenAI GPT-4o mini with Structured Outputs.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your real OPENAI_API_KEY
   ```

3. **Run the test engine:**
   ```bash
   python test_engine.py
   ```

4. **Run the FastAPI server (optional):**
   ```bash
   uvicorn app.main:app --reload
   ```
   Then hit `POST /api/predict` with a match bundle JSON body.

## Project Structure

```
pickup_ai/
├── app/
│   ├── api/routes/predictions.py   # POST /api/predict endpoint
│   ├── core/config.py              # Environment config (pydantic-settings)
│   ├── data/data_simulator.py      # Match bundle generator
│   ├── schemas/prediction.py       # Pydantic response schema
│   ├── services/ai_predictor.py    # GPT-4o mini predictor
│   └── main.py                     # FastAPI app entry
├── test_engine.py                  # CLI test runner (3 bundles)
├── requirements.txt
├── .env.example
└── README.md
```

## Match Bundles

The test engine generates 3 bundles:
- **Top-table clash**: Arsenal vs Man City
- **Relegation battle**: Burnley vs Sheffield United
- **Mid-table game**: Wolves vs Bournemouth

## API Usage

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "match_info": {"home": "Arsenal", "away": "Man City", "date": "2026-03-01"},
    "home_team_context": {"form": "W-W-W-D-L", "avg_goals": 2.1, "injuries": ["Odegaard (Questionable)"]},
    "away_team_context": {"form": "W-L-W-W-W", "avg_goals": 1.9, "injuries": ["De Bruyne (Out)"]},
    "h2h_context": "Man City has won 4 of the last 5 meetings.",
    "news_context": "Saka is fully fit and expected to start."
  }'
```
