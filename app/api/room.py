from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app import crud, schemas

app = FastAPI()

# ルーム一覧取得
@app.get("/rooms", response_model=List[schemas.Room])
async def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms

# ルーム登録
@app.post("/rooms", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)