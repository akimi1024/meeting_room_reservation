from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(12), unique=True, index=True)

    bookings = relationship("Booking", back_populates="user")

class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String(12), unique=True, index=True)
    capacity = Column(Integer)

    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id", ondelete="SET NULL"), nullable=False)
    booked_num = Column(Integer)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
