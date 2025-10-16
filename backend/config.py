
"""Simple config placeholder."""
import os

class Settings:
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

settings = Settings()
