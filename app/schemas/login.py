from pydantic import BaseModel, Field
from app.schemas.user import User

class Login(BaseModel):
    username: str = Field(max_length=12)
    password: str = Field(min_length=6, max_length=12)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User