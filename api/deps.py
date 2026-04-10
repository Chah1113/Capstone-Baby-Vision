from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import AsyncSessionLocal
from core.security import decode_access_token


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_current_user_id(authorization: str = Header(...)) -> int:
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    return int(payload.get("sub"))
