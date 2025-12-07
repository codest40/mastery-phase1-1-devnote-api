from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models import DevNote as Note
from schemas import NoteCreate, NoteUpdate

async def create_note(db: AsyncSession, note_in: NoteCreate) -> Note:
    note = Note(title=note_in.title, content=note_in.content, is_public=note_in.is_public)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note

async def get_note(db: AsyncSession, note_id: int) -> Optional[Note]:
    result = await db.execute(select(Note).where(Note.id == note_id))
    return result.scalars().first()

async def list_notes(db: AsyncSession, limit: int = 50, offset: int = 0) -> List[Note]:
    result = await db.execute(select(Note).order_by(Note.created_at.desc()).limit(limit).offset(offset))
    return result.scalars().all()

async def update_note(db: AsyncSession, note_id: int, note_in: NoteUpdate) -> Optional[Note]:
    note = await get_note(db, note_id)
    if not note:
        return None
    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content
    if note_in.is_public is not None:
        note.is_public = note_in.is_public
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note

async def delete_note(db: AsyncSession, note_id: int) -> bool:
    note = await get_note(db, note_id)
    if not note:
        return False
    await db.delete(note)
    await db.commit()
    return True
