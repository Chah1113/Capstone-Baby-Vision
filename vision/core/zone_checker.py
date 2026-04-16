"""
위험 구역 침범 판별 모듈
- Shapely 라이브러리로 다각형 내 좌표 포함 여부 계산
"""

from shapely.geometry import Polygon
from shapely.geometry import box as make_box


class DangerZone:
    """하나의 위험 구역을 표현하는 클래스"""

    def __init__(self, zone_id: int, name: str, points: list[list[float]]):
        """
        Args:
            zone_id: 구역 고유 ID (DangerZone.id)
            name: 구역 이름 (예: "주방")
            points: 정규화 좌표 리스트 [[x, y], ...] (0.0~1.0)
        """
        self.zone_id = zone_id
        self.name = name
        self.points = points
        if not points or len(points) < 3:
            raise ValueError(f"위험구역 포인트가 3개 미만입니다: {len(points) if points else 0}개")
        self.polygon = Polygon(points)



class ZoneManager:
    """여러 위험 구역을 관리하는 매니저 클래스"""

    def __init__(self):
        self.zones: dict[int, DangerZone] = {}

    def load_zones(self, zone_list: list[dict]):
        """
        서버에서 받은 구역 목록을 로드한다.

        Args:
            zone_list: [{"zone_id": int, "name": str, "points": [[x,y], ...]}, ...]
        """
        self.zones.clear()
        for z in zone_list:
            zone = DangerZone(
                zone_id=z["zone_id"],
                name=z["name"],
                points=z["points"],
            )
            self.zones[zone.zone_id] = zone

    def check_intrusion(
        self, x1: int, y1: int, x2: int, y2: int, frame_width: int, frame_height: int
    ) -> list[DangerZone]:
        """
        탐지된 객체의 바운딩 박스가 위험 구역과 겹치는지 확인한다.

        Args:
            x1, y1, x2, y2: 바운딩 박스 픽셀 좌표
            frame_width: 프레임 가로 크기
            frame_height: 프레임 세로 크기

        Returns:
            침범한 구역 리스트
        """
        if frame_width <= 0 or frame_height <= 0:
            return []

        # 픽셀 좌표 → 정규화 좌표 변환
        detection_box = make_box(
            x1 / frame_width,
            y1 / frame_height,
            x2 / frame_width,
            y2 / frame_height,
        )

        intruded = []
        for zone in self.zones.values():
            if zone.polygon.intersects(detection_box):
                intruded.append(zone)

        return intruded
