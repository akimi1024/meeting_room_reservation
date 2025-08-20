from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(max_length=12)
    password_hash: str
    is_admin: bool

class User(UserCreate):
    user_id: int

    model_config = {
        "from_attributes": True
    }