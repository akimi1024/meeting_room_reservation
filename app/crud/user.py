from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import User as schema_User

# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# ユーザー登録
def create_user(db: Session, user: schema_User):
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザー情報更新
def update_user(db: Session, user: schema_User, user_id: int):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db.query(User).filter(User.username == user.username, User.user_id != user_id).first():
        raise HTTPException(status_code=400, detail="User name already in use")

    db_user.username = user.username
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザー削除
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user
