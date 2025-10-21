from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    is_public: Optional[bool] = False

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = None

class NoteOut(BaseModel):
    id: int
    title: str
    content: Optional[str]
    is_public: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
