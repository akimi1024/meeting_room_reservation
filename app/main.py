from fastapi import FastAPI
from app.api import user, room, booking

app = FastAPI()

app.include_router(user.app, prefix="/api", tags=["users"])
app.include_router(room.app, prefix="/api", tags=["rooms"])
app.include_router(booking.app, prefix="/api", tags=["bookings"])