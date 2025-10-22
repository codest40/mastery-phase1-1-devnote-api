from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import notes
from config import setup_loggers as configure_logging, settings
from db import engine, Base
import asyncio
import logging

configure_logging(settings.log_level)
app = FastAPI(title="DevNotes API", version="0.1.0")
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Templates
templates = Jinja2Templates(directory="app/templates")

app.include_router(notes.router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("notes.html", {"request": request})

@app.on_event("startup")
async def on_startup():
    logging.getLogger("uvicorn").info("Starting up - creating DB tables if not present (dev only)")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    logging.getLogger("uvicorn").info("Shutting down - closing resources")
    await engine.dispose()  # Close DB connection pool cleanly
