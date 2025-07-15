from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.crud.room import get_rooms, create_room as create_room_logic
from app.schemas.room import Room, RoomCreate

router = APIRouter()

# ルーム一覧取得
@router.get("/rooms", response_model=List[Room])
async def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = get_rooms(db, skip=skip, limit=limit)
    return rooms

# ルーム登録
@router.post("/rooms", response_model=Room)
async def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return create_room_logic(db=db, room=room)