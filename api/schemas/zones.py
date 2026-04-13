from pydantic import BaseModel


class DangerZoneCreate(BaseModel):
    camera_id: int
    label: str | None = None
    zone_points: list[list[float]]
