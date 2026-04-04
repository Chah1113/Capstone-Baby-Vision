"""
위험 구역 CRUD API
- docs/api_specs.md 기준
"""

from fastapi import APIRouter

router = APIRouter(tags=["zones"])


@router.get("/zones")
async def get_zones():
    """구역 목록 조회"""
    # TODO: DB에서 구역 목록 가져오기
    return {"zones": []}


@router.post("/zones")
async def create_zone(zone: dict):
    """구역 생성"""
    # TODO: DB에 구역 저장, zone_id 생성
    return {"message": "구역 생성 완료", "zone_id": "zone_xxx"}


@router.delete("/zones/{zone_id}")
async def delete_zone(zone_id: str):
    """구역 삭제"""
    # TODO: DB에서 구역 삭제
    return {"message": f"{zone_id} 삭제 완료"}
