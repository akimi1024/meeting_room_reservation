from fastapi import FastAPI
from app.api import user, room, booking, login
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(room.router, prefix="/api", tags=["rooms"])
app.include_router(booking.router, prefix="/api", tags=["bookings"])
app.include_router(login.router, prefix="/api", tags=["login"])
