# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.db.base import Base
from app.api.routes import contract

app = FastAPI(
    title="Contract Management API",
    version="1.0.0",
    description="Production-ready contract management backend.",
)

# Allow React dev server during development.
# Tighten allow_origins to your real domain(s) before going to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables() -> None:
    """
    Creates all tables that don't yet exist.
    Fine for development and small deployments.
    Use Alembic migrations in production so schema changes are versioned.
    """
    Base.metadata.create_all(bind=engine)


# Register routers
app.include_router(contract.router, prefix="/api")


@app.get("/health", tags=["Health"])
def health() -> dict:
    return {"status": "ok"}