from pydantic import BaseModel, Field

class RoomCreate(BaseModel):
    room_name: str = Field(max_length=12)
    capacity: int

class Room(RoomCreate):
    room_id: int

    class Config:
        orm_mode = True