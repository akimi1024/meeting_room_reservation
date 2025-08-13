from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import User as schema_User
from app.schemas.login import Login as schema_Login
from app.core.security import get_password_hash, verify_password

# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# ユーザー登録
def create_user(db: Session, user: schema_User):
    db_user = User(username=user.username, password_hash=get_password_hash(user.password_hash), is_admin=user.is_admin)
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
    db_user.is_admin = user.is_admin

    # パスワードが来ていればハッシュ化して保存
    if "password" in user:
        db_user.password_hash = get_password_hash(user.password_hash)

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