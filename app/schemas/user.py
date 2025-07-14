from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(max_length=12)

class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True