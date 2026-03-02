"""
Pickup AI — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes.predictions import router as predictions_router
from app.core.database import init_db, check_db_connection


# ── Lifespan ───────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    init_db()
    yield


# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Pickup AI",
    description="AI-powered sports betting prediction engine",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(predictions_router)


# ── Health Check ───────────────────────────────────────────────────────────────


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    Reports service status, database connectivity, and active LLM provider.
    """
    from app.core.config import get_settings

    settings = get_settings()
    db_ok = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "service": "Pickup AI",
        "version": "0.3.0",
        "database": "connected" if db_ok else "unreachable",
        "llm_provider": settings.MODEL_PROVIDER,
        "llm_model": settings.get_litellm_model(),
    }
