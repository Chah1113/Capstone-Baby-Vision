from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from deps import get_db
from db.models import Camera, DetectionEvent, Alert
from schemas.events import EventCreate

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", status_code=201)
async def receive_event(body: EventCreate, db: AsyncSession = Depends(get_db)):
    """vision 서비스 전용 — 감지 이벤트 수신 및 Alert 생성 (Docker 내부 네트워크 전용)"""

    result = await db.execute(select(Camera).where(Camera.id == body.camera_id))
    camera = result.scalar_one_or_none()

    if not camera:
        raise HTTPException(status_code=400, detail="존재하지 않는 카메라예요")

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

    alert = Alert(
        user_id=camera.user_id,
        detection_id=event.id,
        message=f"{body.zone_name}에 아기가 감지됐어요",
    )
    db.add(alert)
    await db.commit()
    return {"ok": True}
