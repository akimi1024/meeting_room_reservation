from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import models
from app.schemas import schemas

# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
    db_booked = db.query(models.Booking).\
          filter(models.Booking.room_id == booking.room_id,
                models.Booking.start_datetime < booking.end_datetime,
                models.Booking.end_datetime > booking.start_datetime).all()

    if len(db_booked) == 0:
      db_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        booked_num=booking.booked_num,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime
      )
      db.add(db_booking)
      db.commit()
      db.refresh(db_booking)
      return db_booking
    else:
        raise HTTPException(
            status_code=404,
            detail="The room is already booked for the selected time."
        )