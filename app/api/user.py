from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.crud.user import get_users
from app.crud.user import create_user as create_user_logic
from app.crud.user import update_user as update_user_logic
from app.schemas.user import User, UserCreate

router = APIRouter()

# ユーザー一覧取得
@router.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

# ユーザー登録
@router.post("/users", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_logic(db=db, user=user)

# ユーザー情報更新
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    print(f"Updating user with ID: {user_id} and data: {user}")
    return update_user_logic(db=db, user=user, user_id=user_id)