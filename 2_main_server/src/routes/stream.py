"""
스트림 URL 관리 API
"""

from fastapi import APIRouter

router = APIRouter(tags=["stream"])

# TODO: 설정 파일 또는 환경변수에서 읽기
BRIDGE_STREAM_URL = "http://localhost:9000/live"


@router.get("/stream/url")
async def get_stream_url():
    """실시간 영상 스트림 URL 반환"""
    return {"stream_url": BRIDGE_STREAM_URL}
