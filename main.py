from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
import crud, notes
from error import  err_router, error_tracking_middleware, global_exception_handler
from fastapi.exceptions import RequestValidationError
from config import setup_loggers as configure_logging, settings
from db import engine, Base, get_db
import asyncio
import logging

configure_logging(settings.log_level)

app = FastAPI(title="DevNotes API", version="0.1.0")

# ✅ Register middleware
app.middleware("http")(error_tracking_middleware)

# ✅ Register global exception handler
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)

# Static + templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include router
app.include_router(notes.router)
app.include_router(err_router)


@app.get("/")
async def root(request: Request, db: AsyncSession = Depends(get_db)):
    notes = await crud.list_notes(db)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})

@app.get("/favicon.ico")
async def root(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("favicon.ico", {"request": request})


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
