from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from deps import get_db, get_current_user_id
from db.models import DangerZone, Camera
from schemas.zones import DangerZoneCreate, DangerZoneUpdate

router = APIRouter(prefix="/danger-zones", tags=["danger_zones"])


async def _get_camera_or_404(camera_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(select(Camera).where(Camera.id == camera_id, Camera.user_id == user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="카메라를 찾을 수 없어요")


@router.post("")
async def create_danger_zone(
    body: DangerZoneCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await _get_camera_or_404(body.camera_id, user_id, db)

    zone = DangerZone(
        camera_id=body.camera_id,
        label=body.label,
        zone_points=body.zone_points
    )
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return {"id": zone.id, "camera_id": zone.camera_id, "label": zone.label, "zone_points": zone.zone_points}


@router.get("/internal/{camera_id}")
async def get_zones_internal(camera_id: int, db: AsyncSession = Depends(get_db)):
    """vision 서비스 전용 — 인증 없이 특정 카메라의 위험구역 반환 (Docker 내부 네트워크 전용)"""
    result = await db.execute(select(DangerZone).where(DangerZone.camera_id == camera_id))
    zones = result.scalars().all()
    return [
        {
            "zone_id": z.id,
            "name": z.label or f"Zone {z.id}",
            "points": z.zone_points,
        }
        for z in zones
    ]


@router.get("/{camera_id}")
async def get_danger_zones(
    camera_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await _get_camera_or_404(camera_id, user_id, db)

    result = await db.execute(select(DangerZone).where(DangerZone.camera_id == camera_id))
    zones = result.scalars().all()
    return [
        {
            "id": z.id,
            "camera_id": z.camera_id,
            "label": z.label,
            "zone_points": z.zone_points,
        }
        for z in zones
    ]


@router.put("/{zone_id}")
async def update_danger_zone(
    zone_id: int,
    body: DangerZoneUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(
        select(DangerZone)
        .join(Camera, DangerZone.camera_id == Camera.id)
        .where(DangerZone.id == zone_id, Camera.user_id == user_id)
    )
    zone = result.scalar_one_or_none()

    if not zone:
        raise HTTPException(status_code=404, detail="위험구역을 찾을 수 없어요")

    zone.label = body.label
    zone.zone_points = body.zone_points
    await db.commit()
    await db.refresh(zone)
    return {"id": zone.id, "camera_id": zone.camera_id, "label": zone.label, "zone_points": zone.zone_points}


@router.delete("/{zone_id}")
async def delete_danger_zone(
    zone_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(
        select(DangerZone)
        .join(Camera, DangerZone.camera_id == Camera.id)
        .where(DangerZone.id == zone_id, Camera.user_id == user_id)
    )
    zone = result.scalar_one_or_none()

    if not zone:
        raise HTTPException(status_code=404, detail="위험구역을 찾을 수 없어요")

    await db.delete(zone)
    await db.commit()
    return {"detail": "삭제됐어요"}
