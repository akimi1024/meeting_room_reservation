from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.crud.room import get_rooms
from app.crud.room import create_room as create_room_logic
from app.crud.room import update_room as update_room_logic
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

# ユーザー更新
@router.put("/rooms/{room_id}", response_model=Room)
async def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    print(f"Updating room with ID: {room_id} and data: {room}")
    return update_room_logic(db=db, room=room, room_id=room_id)