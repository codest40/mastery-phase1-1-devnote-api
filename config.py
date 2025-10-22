import os, logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# =========================
#   DB + ENV SETTINGS
# =========================
class Settings(BaseSettings):
    # URLs
    database_url: str | None = None           # local (Docker)
    external_db_url: str | None = None        # cloud DB (AWS, GitHub Actions, etc.)
    db_url_internal: str | None = None        # Render internal DB

    # Environment flags (auto-detect)
    environment: str | None = None
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# =========================
#  AUTO-DETECT ENVIRONMENT
# =========================
# If Render sets RENDER=true automatically, else fallback to dev
render_flag = os.environ.get("RENDER", "").lower() == "true"
if render_flag:
  db_url_internal = os.environ.get("DB_URL_INTERNAL", "")

env = (
    settings.environment
    or ("render" if render_flag else None)
    or os.environ.get("ENVIRONMENT", "")
    or "local" 
).lower()

print(f"Environmental Variable Found: {env}")

# =========================
#   DB SELECTION LOGIC
# =========================
if env == "render":
    db_url = settings.db_url_internal
elif env in ("github", "aws", "cicd"):
    db_url = settings.external_db_url
else:
    db_url = settings.database_url  # Default local (Docker dev)

DB_URL = db_url

# =========================
#   VALIDATION
# =========================
if not DB_URL:
    raise ValueError(
        f"❌ No database URL found for environment '{env}'. "
        "Define one of: DATABASE_URL, EXTERNAL_DB_URL, INTERNAL_DB_URL."
    )

if DB_URL.startswith("postgresql://") and "asyncpg" not in DB_URL:
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    print("Auto-converted DB URL to asyncpg dialect for SQLAlchemy async support.")

#if "asyncpg" not in DB_URL:
#    raise ValueError(f"❌ Invalid DB URL: must use async driver (asyncpg). Got: {db_url}")



# =========================
#   LOGGING CONFIG
# =========================
base_log_dir = Path("logs")
base_log_dir.mkdir(parents=True, exist_ok=True)

# Define all your log names
LOG_TYPES = ["security", "audit", "admin", "error", "access", "event", "system"]


def setup_loggers(level: str):
    """Initialize loggers with rotation and per-log directories."""
    for log_name in LOG_TYPES:
        # Create subdir per log type
        log_subdir = base_log_dir / log_name
        log_subdir.mkdir(parents=True, exist_ok=True)

        log_path = log_subdir / f"{log_name}.log"

        logger = logging.getLogger(log_name)
        logger.setLevel(level.upper())

        # 5 MB rotation, keep 5 backups
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)

            # Optional: also log to stdout for key logs
            if log_name in ["error", "system", "audit"]:
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(formatter)
                logger.addHandler(stream_handler)


def get_logger(name: str):
    """Retrieve a named logger by its name."""
    if name not in LOG_TYPES:
        raise ValueError(f"Unknown logger: {name}. Available: {LOG_TYPES}")
    return logging.getLogger(name)


# =========================
#   INITIALIZE ON IMPORT
# =========================
setup_loggers(settings.log_level)
