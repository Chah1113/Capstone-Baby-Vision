from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from deps import get_db, get_current_user_id
from db.models import User, Alert
from schemas.users import UserCreate, UserLogin, TokenResponse, RefreshRequest, UserProfileUpdate, UserPasswordUpdate, UserDeleteRequest
from core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_refresh_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일이에요")

    user = User(
        email=body.email,
        password_hash=hash_password(body.password),
        name=body.name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "email": user.email}


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸어요")

    payload = {"sub": str(user.id)}
    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    payload = decode_refresh_token(body.refresh_token)
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="유효하지 않은 리프레시 토큰이에요")

    result = await db.execute(select(User).where(User.id == int(sub)))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=401, detail="존재하지 않는 유저예요")

    new_payload = {"sub": sub}
    return {
        "access_token": create_access_token(new_payload),
        "refresh_token": create_refresh_token(new_payload),
    }


@router.get("/me")
async def get_me(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없어요")

    return {"id": user.id, "email": user.email, "name": user.name}


@router.patch("/me")
async def update_profile(
    body: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없어요")

    user.name = body.name
    await db.commit()
    return {"id": user.id, "email": user.email, "name": user.name}


@router.patch("/me/password")
async def update_password(
    body: UserPasswordUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없어요")

    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="현재 비밀번호가 틀렸어요")

    user.password_hash = hash_password(body.new_password)
    await db.commit()
    return {"detail": "비밀번호가 변경됐어요"}


@router.delete("/me")
async def delete_account(
    body: UserDeleteRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없어요")

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=400, detail="비밀번호가 틀렸어요")

    # Alert 먼저 삭제 — User 삭제(CASCADE)와 DetectionEvent 삭제(SET NULL)가
    # 같은 Alert 행을 동시에 건드리는 충돌 방지
    await db.execute(delete(Alert).where(Alert.user_id == user_id))
    await db.delete(user)
    await db.commit()
    return {"detail": "탈퇴됐어요"}
