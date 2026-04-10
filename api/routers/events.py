from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from db.base import AsyncSessionLocal
from db.models import Camera, DetectionEvent, Alert

router = APIRouter(prefix="/events", tags=["events"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


class EventCreate(BaseModel):
    camera_id: int
    event_type: str
    zone_id: str
    zone_name: str
    confidence: float
    bbox: list


@router.post("", status_code=201)
async def receive_event(body: EventCreate, db: AsyncSession = Depends(get_db)):
    """vision 서비스 전용 — 감지 이벤트 수신 및 Alert 생성 (Docker 내부 네트워크 전용)"""

    # 1. DetectionEvent 저장
    event = DetectionEvent(
        camera_id=body.camera_id,
        event_type=body.event_type,
        zone_id=body.zone_id,
        zone_name=body.zone_name,
        confidence=body.confidence,
        bbox=body.bbox,
    )
    db.add(event)
    await db.flush()  # event.id 확보

    # 2. 카메라 소유자 조회
    result = await db.execute(select(Camera).where(Camera.id == body.camera_id))
    camera = result.scalar_one_or_none()

    if camera:
        alert = Alert(
            user_id=camera.user_id,
            detection_id=event.id,
            message=f"{body.zone_name}에 아기가 감지됐어요",
        )
        db.add(alert)

    await db.commit()
    return {"ok": True}
