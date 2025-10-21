from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_URL

# 1. Create async engine
engine = create_async_engine(DB_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# 3. Declare base class for ORM models
Base = declarative_base()

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
