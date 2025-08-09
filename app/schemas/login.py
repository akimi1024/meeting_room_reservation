from pydantic import BaseModel, Field

class Login(BaseModel):
    username: str = Field(max_length=12)