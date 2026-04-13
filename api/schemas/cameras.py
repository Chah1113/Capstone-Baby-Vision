from pydantic import BaseModel


class CameraCreate(BaseModel):
    name: str


class CameraUpdate(BaseModel):
    is_active: bool
