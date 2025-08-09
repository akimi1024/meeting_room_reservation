from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(max_length=12)
    is_admin: bool

class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True