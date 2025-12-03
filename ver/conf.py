import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pydantic import BaseSettings


# =========================
#   APP + ENV SETTINGS
# =========================
class Settings(BaseSettings):
    database_url: str
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


db_config = Settings()


# =========================
#   LOGGING CONFIG
# =========================
base_log_dir = Path("logs")
base_log_dir.mkdir(parents=True, exist_ok=True)

# Map each logger name to its subfolder and filename
LOG_PATHS = {
    "secLogger": ("sec", "security.log"),
    "auditLogger": ("audit", "audit.log"),
    "adminLogger": ("admin", "admin.log"),
    "errorLogger": ("error", "error.log"),
    "accessLogger": ("access", "access.log"),
    "eventLogger": ("event", "event.log"),
    "systemLogger": ("system", "system.log"),
}


def create_logger(name: str, subfolder: str, filename: str, level: str):
    """Create a rotating logger inside its own subdirectory."""
    log_subdir = base_log_dir / subfolder
    log_subdir.mkdir(parents=True, exist_ok=True)
    log_path = log_subdir / filename

    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


# =========================
#   CREATE ALL LOGGERS
# =========================
secLogger = create_logger("security", "sec", "security.log", db_config.log_level)
auditLogger = create_logger("audit", "audit", "audit.log", db_config.log_level)
adminLogger = create_logger("admin", "admin", "admin.log", db_config.log_level)
errorLogger = create_logger("error", "error", "error.log", db_config.log_level)
accessLogger = create_logger("access", "access", "access.log", db_config.log_level)
eventLogger = create_logger("event", "event", "event.log", db_config.log_level)
systemLogger = create_logger("system", "system", "system.log", db_config.log_level)
