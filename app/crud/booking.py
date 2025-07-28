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

# 予約更新
def update_booking(db: Session, booking: schemas_booking, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    conflict_booking = db.query(Booking).filter(
                        Booking.room_id == booking.room_id,
                        Booking.booking_id != booking_id,
                        Booking.start_datetime < booking.end_datetime,
                        Booking.end_datetime > booking.start_datetime
                        ).first()
    if conflict_booking:
      raise HTTPException(status_code=404, detail="The meeting room is already reserved at the specified time")

    db_booking.user_id = booking.user_id
    db_booking.room_id = booking.room_id
    db_booking.booked_num = booking.booked_num
    db_booking.start_datetime = booking.start_datetime
    db_booking.end_datetime = booking.end_datetime

    db.commit()
    db.refresh(db_booking)

    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="booking not found")

    db.delete(db_booking)
    db.commit()
    return db_booking
