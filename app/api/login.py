from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud.login import login_user as logic_user_logic
from app.schemas.user import User
from app.schemas.login import Login

router = APIRouter()

# ログインユーザー情報取得
@router.post("/login", response_model=User)
async def read_user(login: Login, db: Session = Depends(get_db)):
  return logic_user_logic(db=db, login=login)