from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "change_this_to_env_secret"   # 本番は envvar に入れる
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 例：60分

def get_password_hash(password: str) -> str:
    return PWD_CTX.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return PWD_CTX.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded
