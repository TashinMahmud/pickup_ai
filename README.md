# 📈 Pickup AI — Sports Betting Prediction Quant Engine

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](#prerequisites)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Multi--Provider-EE5253?style=for-the-badge)](#litellm-multi-provider-interface)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white)](#database-persistence)

---

**Pickup AI** is a professional-grade sports betting quant engine built on **FastAPI** and **LiteLLM**. It parses multi-sport match bundles (Football, Basketball, Tennis), executes analytical prediction runs across multiple AI providers (OpenAI, Gemini, Anthropic), converts bookmaker prices into implied probabilities to identify value edges, and logs results to a PostgreSQL database.

</div>

---

## 🛠️ Technical Architecture

Pickup AI functions as an isolated prediction server that consumes match statistics and outputs structured valuation forecasts.

```
+-------------------------------------------------------------+
|                      CLIENT INGESTION                       |
|   Sends Raw Match Bundle (Stats, Injury Reports, Odds)      |
+------------------------------+------------------------------+
                               | (HTTP POST /api/predict)
                               v
+-------------------------------------------------------------+
|                    FASTAPI ENGINE CORE                      |
|  Initializes connections, routes calls, handles exceptions   |
+------------------------------+------------------------------+
                               |
                               +------------------------------+
                               |                              |
                               v                              v
+------------------------------+------+       +---------------+---------------+
|       LITELLM PREDICTOR SERVICE     |       |      DATABASE PERSISTENCE     |
| - Custom sport-specific prompts     | <---> | - PostgreSQL Logging          |
| - OpenAI / Gemini / Anthropic       |       | - SQLAlchemy ORM Table        |
+-------------------------------------+       +-------------------------------+
```

### Core Code Modules & Responsibilities

*   `app/api/` Layer:
    *   [`routes/predictions.py`](app/api/routes/predictions.py): Exposes the prediction route, triggers LLM evaluation run, and commits the prediction record to PostgreSQL.
*   `app/core/` Layer:
    *   [`config.py`](app/core/config.py): Configuration loading and structured LiteLLM provider model resolver.
    *   [`database.py`](app/core/database.py): Base engine, table initializers, and PostgreSQL connection health checks.
*   `app/services/` Layer:
    *   [`ai_predictor.py`](app/services/ai_predictor.py): Compiles sport-specific system prompts (Football, Basketball, Tennis), initializes LiteLLM, executes structured schema completions, and normalizes provider errors.
*   `app/model/` & `schemas/` Layer:
    *   [`prediction.py` (Model)](app/model/prediction.py): SQLAlchemy mapping representing a committed sports prediction.
    *   [`prediction.py` (Schemas)](app/schemas/prediction.py): Pydantic input models verifying payload constraints and enforcing odds converters.

---

## ⚡ Core Integration Interfaces

<details>
<summary><b>🤖 LiteLLM Multi-Provider Interface</b></summary>

Allows seamless switching between models like `gpt-4o-mini`, `gemini-2.0-flash`, or `claude-3-5-haiku-latest` simply by modifying the `MODEL_PROVIDER` key in the environment configuration, standardizing structural response formats regardless of the selected AI provider.
</details>

<details>
<summary><b>⚽ Sport-Specific Signal Weighting</b></summary>

The system uses customized reasoning guides for different sports:
*   **Football**: Evaluates key player absences, venue records, H2H statistics, and xG averages.
*   **Basketball**: Weightings for schedule fatigue (e.g., Back-to-Back nights), player rest profiles, and team pace indexes.
*   **Tennis**: Evaluates court surface parameters, hold percentages, and physical match fatigue.
</details>

<details>
<summary><b>📊 Implied Probability & Value Edge Math</b></summary>

When bookmaker odds are supplied, the engine calculates the implied probability ($implied = 1 / odds$) and matches it against the model's confidence level. If the model's certainty exceeds the bookmaker's pricing, the difference is flagged as a positive edge (e.g., `+14.3% edge`) and logged.
</details>

---

## 🚀 Getting Started

### 1. Requirements
*   Python 3.10+
*   PostgreSQL Instance (Local or cloud-hosted)
*   Active API keys for chosen provider (OpenAI / Gemini)

### 2. Configurations Setup
1.  Copy `.env.example` to a new `.env` file:
    ```bash
    cp .env.example .env
    ```
2.  Populate your credentials:
    ```env
    MODEL_PROVIDER=openai
    MODEL_NAME=gpt-4o-mini
    OPENAI_API_KEY=sk-your-openai-key-here
    DATABASE_URL=postgresql://postgres:password@localhost:5432/pickup_db
    PORT=8000
    ```

### 3. Dependency Ingestion & Run
Build the environment and install requirements:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Start the FastAPI application:
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive API docs will be active at `http://localhost:8000/docs`.

### 4. Running Test Scenarios
You can run the simulated match bundle prediction test to verify your configurations:
```bash
python scenario_test.py
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
