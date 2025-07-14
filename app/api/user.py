from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app import crud, schemas

app = FastAPI()

# ユーザー一覧取得
@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# ユーザー登録
@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)