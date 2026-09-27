"""
Application configuration.

All settings come from environment variables, with sensible defaults for
local development. Copy `.env.example` to `.env` inside `backend/` and
adjust values there -- never commit the real `.env` file (see the root
`.gitignore`).
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# This file lives at backend/app/config.py, so three parents up is the
# project root (the "BBD/" folder that contains backend/, frontend/,
# database/, etc). Computing this from __file__ -- instead of assuming a
# particular working directory -- means the app finds the right paths no
# matter where `uvicorn` is launched from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "database" / "bbd_hunter.db"

# `.as_posix()` renders the path with forward slashes even on Windows
# (e.g. "C:/Users/you/BBD/database/bbd_hunter.db"). That happens to be
# exactly the form SQLAlchemy expects after the "sqlite:///" prefix, on
# both Windows and Linux/Mac, so we don't need to hand-build a different
# URL per platform.
DEFAULT_DATABASE_URL = f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"


class Settings(BaseSettings):
    """Typed application settings, populated from environment variables.

    Field names map to env vars case-insensitively, e.g. `database_url`
    reads the `DATABASE_URL` environment variable.
    """

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / "backend" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- General ---
    app_name: str = "bbd-hunter"
    app_version: str = "0.1.0"
    environment: str = "development"  # "development" or "production"
    debug: bool = True

    # --- Database ---
    database_url: str = DEFAULT_DATABASE_URL

    # --- CORS ---
    # Comma-separated list of origins allowed to call this API. The
    # defaults match Vite's default dev server ports.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        """`cors_origins` split into a clean list for CORSMiddleware."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# A single shared Settings instance, imported by the rest of the app.
settings = Settings()
