"""
이벤트 브로커
- AI가 보낸 "위험 감지!" 신호를 메인 서버로 전달
- 지금은 HTTP 방식만 구현 (나중에 Redis/WebSocket 추가 가능)
"""

import requests
from config import MAIN_SERVER_URL, EVENT_ENDPOINT


def forward_event(event: dict) -> bool:
    """
    위험 감지 이벤트를 메인 서버로 전달한다.

    Args:
        event: event_schemas.json의 alert_event 형식

    Returns:
        전달 성공 여부
    """
    url = f"{MAIN_SERVER_URL}{EVENT_ENDPOINT}"

    try:
        response = requests.post(url, json=event, timeout=3)
        print(f"[브로커] 이벤트 전달 완료 → {response.status_code}")
        return response.status_code == 200
    except requests.ConnectionError:
        print(f"[브로커] 서버 연결 실패: {url}")
        return False
    except Exception as e:
        print(f"[브로커] 전달 실패: {e}")
        return False
