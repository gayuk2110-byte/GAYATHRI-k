from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .database import Base, engine
from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="A FastAPI + Jinja2 + SQLite demo using Google's Gemini API.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "FitBuddy"}
