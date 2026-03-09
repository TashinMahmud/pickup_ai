# Pickup AI

AI-powered sports betting prediction engine using OpenAI GPT-4o mini with Structured Outputs and PostgreSQL persistence.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.2
DATABASE_URL=postgresql://user:password@host:5432/dbname
PORT=8000
```

### 3. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

The server will automatically create the `predictions` table on startup.

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok",
  "service": "Pickup AI",
  "version": "0.2.0",
  "database": "connected"
}
```

### Predict (POST /api/predict)

Send a match bundle → get a prediction + auto-save to Postgres.

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "match_info": {"home": "Arsenal", "away": "Man City", "date": "2026-03-01"},
    "home_team_context": {
      "form": "W-W-W-D-L",
      "avg_goals": 2.1,
      "injuries": ["Odegaard (Questionable)"],
      "home_record": "W8-D2-L1 at Emirates this season",
      "xG_per_game": 2.3
    },
    "away_team_context": {
      "form": "W-L-W-W-W",
      "avg_goals": 1.9,
      "injuries": ["De Bruyne (Out)"],
      "away_record": "W5-D3-L3 on the road this season",
      "xG_per_game": 1.7
    },
    "h2h_context": "Man City won 4 of last 5, but Arsenal won the most recent home game 1-0.",
    "news_context": "Saka fully fit. Arteta confirmed 4-3-3.",
    "league_context": {
      "league": "Premier League",
      "season": "2025-26",
      "avg_goals_per_game": 2.77,
      "home_win_rate": 0.46,
      "draw_rate": 0.24,
      "away_win_rate": 0.30
    },
    "odds": {
      "home_win": 2.10,
      "draw": 3.40,
      "away_win": 3.60,
      "over_2_5": 1.85,
      "under_2_5": 2.00,
      "btts_yes": 1.75,
      "btts_no": 2.10
    }
  }'
```

Response:
```json
{
  "confidence": 76,
  "market": "Match Result",
  "prediction": "Arsenal Win",
  "reasoning": "Given De Bruyne's absence and Arsenal's strong home form, they are favored.",
  "implied_probability": 0.476,
  "value_edge": "+14.2% edge"
}
```

The prediction is **automatically saved** to the `predictions` table in your Postgres database.

### Swagger UI

Visit `http://localhost:8000/docs` for the interactive API documentation.

## Database Schema (predictions table)

| Column | Type | Notes |
|--------|------|-------|
| id | Integer | Primary key, auto-increment |
| match_id | String | Unique — `{home}_vs_{away}_{date}` |
| confidence | Integer | 1-100 |
| market | String | e.g. "Match Result" |
| prediction_value | String | e.g. "Arsenal Win" |
| reasoning | String(120) | Max 120 characters |
| value_edge | String | Nullable, e.g. "+14.2% edge" |
| implied_probability | Float | Nullable, e.g. 0.476 |
| created_at | DateTime | Auto-set to UTC now |

## Project Structure

```
pickup_ai/
├── app/
│   ├── api/routes/predictions.py   # POST /api/predict (with DB save)
│   ├── core/
│   │   ├── config.py               # Environment config
│   │   └── database.py             # SQLAlchemy engine + session
│   ├── model/prediction.py         # SQLAlchemy predictions model
│   ├── schemas/prediction.py       # Pydantic response schema
│   ├── services/ai_predictor.py    # Multi-Sport AI Quant
│   └── main.py                     # FastAPI app entry
├── requirements.txt
├── .env.example
└── README.md
```
