from pydantic import BaseModel


class CameraCreate(BaseModel):
    name: str
