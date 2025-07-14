from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.booking import Booking
from app.schemas.booking import Booking as schemas_booking

# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booking).offset(skip).limit(limit).all()

# 予約登録
def create_booking(db: Session, booking: schemas_booking):
    db_booked = db.query(Booking).\
          filter(Booking.room_id == booking.room_id,
                Booking.start_datetime < booking.end_datetime,
                Booking.end_datetime > booking.start_datetime).all()

    if len(db_booked) == 0:
      db_booking = Booking(
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