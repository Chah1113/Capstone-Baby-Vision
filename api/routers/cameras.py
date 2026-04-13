from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from deps import get_db, get_current_user_id
from db.models import Camera
from schemas.cameras import CameraCreate, CameraUpdate, CameraStatusUpdate
import uuid
import os

router = APIRouter(prefix="/cameras", tags=["cameras"])


def _camera_dict(c: Camera) -> dict:
    webrtc_host = os.getenv("WEBRTC_HOST", os.getenv("SERVER_HOST", "localhost"))
    webrtc_port = os.getenv("WEBRTC_PORT", "8889")
    stream_path = c.stream_url.split("/")[-1]
    return {
        "id": c.id,
        "name": c.name,
        "stream_url": c.stream_url,
        "is_active": c.is_active,
        "is_connected": c.is_connected,
        "webrtc_url": f"http://{webrtc_host}:{webrtc_port}/{stream_path}/whep"
    }


@router.post("")
async def create_camera(
    body: CameraCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    rtsp_host = os.getenv("RTSP_HOST", os.getenv("SERVER_HOST", "localhost"))
    rtsp_port = os.getenv("RTSP_PORT", "8554")
    stream_url = f"rtsp://{rtsp_host}:{rtsp_port}/{uuid.uuid4()}"

    camera = Camera(
        user_id=user_id,
        name=body.name,
        stream_url=stream_url
    )
    db.add(camera)
    await db.commit()
    await db.refresh(camera)
    return _camera_dict(camera)

@router.get("/internal")
async def get_all_cameras_internal(db: AsyncSession = Depends(get_db)):
    """vision 서비스 전용 — 인증 없이 전체 카메라 목록 반환 (Docker 내부 네트워크 전용)"""
    result = await db.execute(select(Camera).where(Camera.is_active == True))
    cameras = result.scalars().all()
    return [_camera_dict(c) for c in cameras]


@router.patch("/internal/{camera_id}/status")
async def update_camera_status(
    camera_id: int,
    body: CameraStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """vision 서비스 전용 — 카메라 연결 상태 갱신 (Docker 내부 네트워크 전용)"""
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(status_code=404, detail="카메라를 찾을 수 없어요")

    camera.is_connected = body.is_connected
    await db.commit()


@router.get("/{camera_id}")
async def get_camera(
    camera_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Camera).where(Camera.id == camera_id, Camera.user_id == user_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(status_code=404, detail="카메라를 찾을 수 없어요")

    return _camera_dict(camera)


@router.get("")
async def get_cameras(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Camera).where(Camera.user_id == user_id, Camera.is_active == True))
    cameras = result.scalars().all()
    return [_camera_dict(c) for c in cameras]


@router.patch("/{camera_id}")
async def update_camera(
    camera_id: int,
    body: CameraUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Camera).where(Camera.id == camera_id, Camera.user_id == user_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(status_code=404, detail="카메라를 찾을 수 없어요")

    camera.is_active = body.is_active
    await db.commit()
    return _camera_dict(camera)


@router.delete("/{camera_id}")
async def delete_camera(
    camera_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Camera).where(Camera.id == camera_id, Camera.user_id == user_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(status_code=404, detail="카메라를 찾을 수 없어요")

    await db.delete(camera)
    await db.commit()
    return {"detail": "삭제됐어요"}
