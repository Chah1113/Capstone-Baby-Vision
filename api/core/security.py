from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY 환경변수가 설정되지 않았어요")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60       # 1시간
REFRESH_TOKEN_EXPIRE_DAYS = 30         # 30일

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰이에요")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰이에요")
    return payload

def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 리프레시 토큰이에요")
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="리프레시 토큰이 아니에요")
    return payload
