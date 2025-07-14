from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app import crud, schemas

app = FastAPI()

# 予約一覧取得
@app.get("/bookings", response_model=List[schemas.Booking])
async def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

# 予約登録
@app.post("/bookings", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)