from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.crud.booking import get_bookings, create_booking as create_booking_logic
from app.crud.booking import update_booking as update_booking_logic
from app.schemas.booking import Booking, BookingCreate

router = APIRouter()

# 予約一覧取得
@router.get("/bookings", response_model=List[Booking])
async def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = get_bookings(db, skip=skip, limit=limit)
    return bookings

# 予約登録
@router.post("/bookings", response_model=Booking)
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_booking_logic(db=db, booking=booking)

# 予約更新
@router.put("/bookings/{booking_id}", response_model=Booking)
async def update_booking(booking_id: int, booking: BookingCreate, db: Session=Depends(get_db)):
    print(f"Updating Booking with ID: {booking_id} and data: {booking}")
    return update_booking_logic(db=db, booking=booking, booking_id=booking_id)