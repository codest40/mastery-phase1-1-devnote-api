from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
import crud, notes
from config import setup_loggers as configure_logging, settings, get_env
from db import engine, Base, get_db
import asyncio
import logging
import time
import platform

configure_logging(settings.log_level)

app = FastAPI(title="DevNotes API", version="0.1.0")

# Static + templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include router
app.include_router(notes.router)


@app.get("/")
async def root(request: Request, db: AsyncSession = Depends(get_db)):
    notes = await crud.list_notes(db)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})

@app.get("/favicon.ico")
async def root(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("favicon.ico", {"request": request})

# === DASHBOARD METRICS ===
@app.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    start = time.perf_counter()
    notes = await crud.list_notes(db)
    latency = (time.perf_counter() - start) * 1000

    stats = {
        "total_notes": len(notes),
        "latency_ms": round(latency, 2),
        "environment": get_env() if not None else "dev",
        "error_count": 0,  # placeholder for now
        "python_version": platform.python_version(),
        "platform": platform.system(),
    }
    return stats


# === STARTUP/SHUTDOWN ===
@app.on_event("startup")
async def on_startup():
    logging.getLogger("uvicorn").info("Starting up - creating DB tables if not present (dev only)")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    logging.getLogger("uvicorn").info("Shutting down - closing resources")
    await engine.dispose()
    print("✅ Database engine disposed — shutdown complete.")
