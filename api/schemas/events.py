from pydantic import BaseModel


class EventCreate(BaseModel):
    camera_id: int
    event_type: str
    zone_id: int
    zone_name: str
    confidence: float
    bbox: list[float]
