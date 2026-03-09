# Pickup AI

An AI-powered sports betting prediction engine using an LLM to generate high-value betting predictions.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   Copy `.env.example` to `.env` and fill in your API key and Postgres connection URL.
   ```bash
   cp .env.example .env
   ```

3. **Start the Server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *(Note: The database tables will be created automatically on startup).*

## API Endpoints

### Health Check (GET /health)
Check service and database connectivity.
```bash
curl http://localhost:8000/health
```

### Predict (POST /api/predict)
Send a match payload (Football, Basketball, or Tennis) to receive a quantized value prediction. The output is automatically saved to the PostgreSQL database.

*See `http://localhost:8000/docs` (Swagger UI) for the exact payload schema while the server is running.*

## Project Structure

```
pickup_ai/
├── app/
│   ├── api/routes/predictions.py   # Prediction endpoint & DB save route
│   ├── core/
│   │   ├── config.py               # Env variable models
│   │   └── database.py             # SQLAlchemy Engine
│   ├── model/prediction.py         # Postgres Prediction Schema
│   ├── schemas/prediction.py       # Pydantic response structs
│   ├── services/ai_predictor.py    # OpenAI Predictor Service
│   └── main.py                     # FastAPI entry point
├── .env.example
├── requirements.txt
└── README.md
```
