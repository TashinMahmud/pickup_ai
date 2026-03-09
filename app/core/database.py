"""
Pickup AI — Database Setup
SQLAlchemy engine, session, and base for PostgreSQL.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import get_settings

settings = get_settings()

# ── Engine ─────────────────────────────────────────────────────────────────────

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # Verify connections before using them
    pool_size=5,              # Connection pool size
    max_overflow=10,          # Extra connections allowed beyond pool_size
)

# ── Session ────────────────────────────────────────────────────────────────────

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Base ───────────────────────────────────────────────────────────────────────

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables defined by SQLAlchemy models."""
    # Import models so they register with Base.metadata
    import app.model.prediction  # noqa: F401
    Base.metadata.create_all(bind=engine)


def check_db_connection() -> bool:
    """Check if the database is reachable."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
