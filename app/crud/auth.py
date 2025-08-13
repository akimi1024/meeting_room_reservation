from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import User as schemaUser
from app.schemas.login import Login
from app.schemas.login import Token
from app.core.security import get_password_hash, verify_password, create_access_token

def login_user(db: Session, login: Login):
    login_user = db.query(User).filter(User.username == login.username).first()
    if not login_user or not verify_password(login.password, login_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token({"sub": str(login_user.user_id), "username": login_user.username, "is_admin": login_user.is_admin})
    return {"access_token": access_token, "token_type": "bearer", "user": login_user}

def signup_user(db: Session, login: Login):
    signup_user = db.query(User).filter(User.username == login.username).first()
    if signup_user:
        raise HTTPException(status_code=400, detail="username already registered")

    db_user = User(username=login.username, password_hash=get_password_hash(login.password), is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": db_user.username})

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=schemaUser.model_validate(db_user)
    )