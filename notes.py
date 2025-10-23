from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import crud, schemas
from db import get_db

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(note_in: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_note(db, note_in)

@router.get("/{note_id}", response_model=schemas.NoteOut)
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.get("/", response_model=List[schemas.NoteOut])
async def list_notes(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await crud.list_notes(db, limit=limit, offset=offset)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud.delete_note(db, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return None

# ============================
# FULL UPDATE (PUT)
# ============================
@router.put("/{note_id}", response_model=schemas.NoteOut)
async def update_note(note_id: int, data: schemas.NoteUpdate, db: AsyncSession = Depends(get_db)):
    """
    PUT = Replace the whole note.
    All missing fields will become NULL.
    """
    note = await crud.update_note(db, note_id, data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Replace all fields
    note.title = data.title
    note.content = data.content
    note.is_public = data.is_public

    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


# ============================
# PARTIAL UPDATE (PATCH)
# ============================
@router.patch("/{note_id}", response_model=schemas.NoteOut)
async def partial_update_note(note_id: int, data: schemas.NoteUpdate, db: AsyncSession = Depends(get_db)):
    """
    PATCH = Update only provided fields.
    Uses exclude_unset=True to ignore missing ones.
    """
    note = await crud.update_note(db, note_id, data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    for field, value in update_data.items():
        setattr(note, field, value)

    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note
