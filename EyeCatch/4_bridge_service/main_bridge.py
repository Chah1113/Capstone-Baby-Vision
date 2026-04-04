"""
브릿지 메인 서버
- AI 프로세스로부터 이벤트를 수신
- 이벤트 브로커를 통해 메인 서버로 전달
- 스트림 프록시와 함께 실행
"""

from fastapi import FastAPI
from event_broker.broker import forward_event_http

app = FastAPI(title="EyeCatch Bridge Service")


@app.post("/event")
async def receive_event(event: dict):
    """
    AI 프로세스로부터 위험 감지 이벤트를 수신한다.
    수신 즉시 메인 서버로 전달.
    """
    print(f"[브릿지] 이벤트 수신: {event.get('event_type')} - {event.get('zone_name')}")
    forward_event_http(event)
    return {"status": "forwarded"}


@app.get("/health")
async def health():
    return {"status": "bridge running"}
