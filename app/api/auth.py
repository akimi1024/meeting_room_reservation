from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud.auth import login_user as login_user_logic
from app.crud.auth import signup_user as signup_user_logic
from app.schemas.user import User
from app.schemas.login import Login, Token

router = APIRouter()

# ログインユーザー情報取得
@router.post("/login", response_model=Token)
async def read_user(login: Login, db: Session = Depends(get_db)):
  return login_user_logic(db=db, login=login)


@router.post("/signup", response_model=Token)
async def signup_user(login: Login, db: Session = Depends(get_db)):
  print(login)
  return signup_user_logic(db=db, login=login)