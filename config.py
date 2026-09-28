import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "FitBuddy")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")

# Current Gemini SDK uses GEMINI_API_KEY.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Keep model names configurable so the project can follow the models available
# to the API key without changing application code.
GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.8-flash")
GEMINI_TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-3.8-flash")

# If false, the app will use a deterministic demo response when no API key exists.
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
