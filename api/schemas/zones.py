from pydantic import BaseModel, field_validator


class DangerZoneCreate(BaseModel):
    camera_id: int
    label: str | None = None
    zone_points: list[list[float]]

    @field_validator("zone_points")
    @classmethod
    def validate_points(cls, v):
        if len(v) < 3:
            raise ValueError("위험구역은 꼭짓점이 3개 이상이어야 합니다")
        for point in v:
            if len(point) != 2:
                raise ValueError("각 좌표는 [x, y] 형식이어야 합니다")
            x, y = point
            if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
                raise ValueError(f"좌표값은 0.0~1.0 범위여야 합니다: [{x}, {y}]")
        return v


class DangerZoneUpdate(BaseModel):
    label: str | None = None
    zone_points: list[list[float]]

    @field_validator("zone_points")
    @classmethod
    def validate_points(cls, v):
        if len(v) < 3:
            raise ValueError("위험구역은 꼭짓점이 3개 이상이어야 합니다")
        for point in v:
            if len(point) != 2:
                raise ValueError("각 좌표는 [x, y] 형식이어야 합니다")
            x, y = point
            if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
                raise ValueError(f"좌표값은 0.0~1.0 범위여야 합니다: [{x}, {y}]")
        return v
