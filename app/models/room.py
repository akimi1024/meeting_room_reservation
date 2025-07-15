from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String(12), unique=True, index=True)
    capacity = Column(Integer)

    bookings = relationship("Booking", back_populates="room")