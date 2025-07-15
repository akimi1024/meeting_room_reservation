from sqlalchemy.orm import Session
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