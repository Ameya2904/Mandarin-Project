"""Environment configuration and app-wide constants."""
import os
from pathlib import Path

from dotenv import load_dotenv

# backend/ — the directory that holds .env (one level above this package).
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]

JWT_SECRET = os.environ["JWT_SECRET_KEY"]
JWT_ALGO = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 43200))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Spaced-repetition stage -> interval in days.
SRS_INTERVALS = {1: 1, 2: 2, 3: 7, 4: 30, 5: 90, 6: 365}
