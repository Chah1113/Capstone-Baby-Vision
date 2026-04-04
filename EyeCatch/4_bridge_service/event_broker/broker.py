"""
이벤트 브로커
- AI의 "위험 감지!" 신호를 메인 서버로 초고속 전달
- HTTP / Redis Pub/Sub / WebSocket 방식 지원

TODO: 브릿지 담당자가 구현
"""

import requests
import json
from typing import Dict

# 설정 (config.yaml에서 읽어오도록 변경 예정)
MAIN_SERVER_EVENT_URL = "http://localhost:8000/api/alerts/event"


def forward_event_http(event: Dict):
    """
    HTTP POST 방식으로 메인 서버에 이벤트를 전달한다.

    Args:
        event: event_schemas.json의 alert_event 형식
    """
    try:
        response = requests.post(
            MAIN_SERVER_EVENT_URL,
            json=event,
            timeout=3,
        )
        print(f"[브로커] 이벤트 전달 완료: {response.status_code}")
    except Exception as e:
        print(f"[브로커] 이벤트 전달 실패: {e}")


# TODO: Redis Pub/Sub 방식
# def forward_event_redis(event: Dict):
#     import redis
#     r = redis.Redis(host="localhost", port=6379)
#     r.publish("eyecatch_alerts", json.dumps(event))


# TODO: WebSocket 방식
# async def forward_event_websocket(event: Dict):
#     pass
