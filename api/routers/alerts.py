from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.base import AsyncSessionLocal
from db.models import Alert, DetectionEvent
from core.security import decode_access_token

router = APIRouter(prefix="/alerts", tags=["alerts"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

def get_current_user_id(authorization: str = Header(...)) -> int:
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    return int(payload.get("sub"))

@router.get("")
async def get_alerts(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(
        select(Alert)
        .where(Alert.user_id == user_id)
        .options(selectinload(Alert.detection_event))
        .order_by(Alert.sent_at.desc())
    )
    alerts = result.scalars().all()

    return [
        {
            "id": a.id,
            "message": a.message,
            "is_read": a.is_read,
            "sent_at": a.sent_at,
            "zone_name": a.detection_event.zone_name if a.detection_event else None,
            "confidence": a.detection_event.confidence if a.detection_event else None,
            "detected_at": a.detection_event.detected_at if a.detection_event else None,
        }
        for a in alerts
    ]

@router.patch("/{alert_id}/read")
async def mark_as_read(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.user_id == user_id))
    alert = result.scalar_one_or_none()

    if not alert:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없어요")

    alert.is_read = True
    await db.commit()
    return {"detail": "읽음 처리됐어요"}
