from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.login import Login

def login_user(db: Session, login: Login):
    login_user = db.query(User).filter(User.username == login.username).first()
    if not login_user:
        raise HTTPException(status_code=404, detail="user not found")

    return login_user