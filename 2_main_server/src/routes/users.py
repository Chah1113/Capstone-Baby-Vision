"""
사용자 / 디바이스 관리 API
"""

from fastapi import APIRouter

router = APIRouter(tags=["users"])


@router.post("/users/fcm-token")
async def register_fcm_token(body: dict):
    """FCM 토큰 등록"""
    fcm_token = body.get("fcm_token")
    # TODO: DB에 토큰 저장
    return {"message": "토큰 등록 완료"}
