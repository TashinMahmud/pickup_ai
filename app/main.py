"""
Pickup AI — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from app.api.routes.predictions import router as predictions_router

app = FastAPI(
    title="Pickup AI",
    description="AI-powered sports betting prediction engine",
    version="0.1.0",
)

app.include_router(predictions_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Pickup AI"}
