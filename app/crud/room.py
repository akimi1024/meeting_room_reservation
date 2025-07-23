from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import Room as schemas_Room

# 会議室一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Room).offset(skip).limit(limit).all()

# 会議室登録
def create_room(db: Session, room: schemas_Room):
    db_room = Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# 会議室更新
def update_room(db: Session, room: schemas_Room, room_id: int):
    db_room = db.query(Room).filter(Room.room_id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    db_room.room_name = room.room_name
    db_room.capacity = room.capacity
    db.commit()
    db.refresh(db_room)
    return db_room