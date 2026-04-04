"""
알림 API
- 브릿지에서 위험 이벤트 수신
- 프론트엔드에 알림 내역 제공
"""

from fastapi import APIRouter

router = APIRouter(tags=["alerts"])


@router.get("/alerts")
async def get_alerts(limit: int = 20, offset: int = 0):
    """알림 내역 조회"""
    # TODO: DB에서 알림 목록 가져오기
    return {"alerts": [], "total": 0}


@router.post("/alerts/event")
async def receive_alert_event(event: dict):
    """
    브릿지로부터 위험 감지 이벤트 수신
    - event_schemas.json의 alert_event 형식 참고
    - 수신 후 FCM 푸시 알림 발송
    """
    # TODO: 이벤트 DB 저장
    # TODO: FCM 푸시 알림 발송 (firebase 모듈 호출)
    return {"message": "이벤트 수신 완료"}
