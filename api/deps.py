from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import AsyncSessionLocal
from core.security import decode_access_token

_bearer = HTTPBearer()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> int:
    payload = decode_access_token(credentials.credentials)
    return int(payload.get("sub"))
