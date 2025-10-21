# ============================================================
#  DEVNOTES API – FastAPI Async Backend (Universal Build)
#  Author: Markam | DevOps/Backend Engineer
# ------------------------------------------------------------
#  Works seamlessly in:
#   - Local development (Docker Compose)
#   - CI/CD pipelines (GitHub Actions)
#   - Production (AWS, Render, etc.)
# ============================================================

# -------------------------
# 1️⃣ Base Image
# -------------------------
FROM python:3.11-slim

WORKDIR /app

# -------------------------
# 2️⃣ System Dependencies
# -------------------------
# Required for PostgreSQL drivers (asyncpg, psycopg2)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# -------------------------
# 3️⃣ Install Python Packages
# -------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------
# 4️⃣ Copy Project Source
# -------------------------
COPY . .

# -------------------------
# 5️⃣ Environment Variables
# -------------------------
ENV PYTHONUNBUFFERED=1 \
    APP_ENV=dev \
    LOG_LEVEL=INFO

# -------------------------
# 6️⃣ Command
# -------------------------
# Uses APP_ENV to decide mode:
# - dev → hot reload
# - prod → normal run (used by CI/CD or deployment)
CMD ["/bin/sh", "-c", \
    "if [ \"$APP_ENV\" = 'prod' ]; then \
        echo 'Running in production mode...'; \
        uvicorn main:app --host 0.0.0.0 --port 8000; \
     else \
        echo 'Running in development mode...'; \
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload; \
     fi"]
