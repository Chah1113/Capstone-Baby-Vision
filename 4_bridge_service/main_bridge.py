"""
EyeCatch 브릿지 메인 서버
- /live  : 카메라 영상을 실시간 MJPEG 스트림으로 중계
- /event : AI로부터 위험 감지 이벤트를 수신 → 메인 서버로 전달
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from stream_proxy.stream import stream
from event_broker.broker import forward_event
from config import BRIDGE_HOST, BRIDGE_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 시작 시 카메라 열기, 종료 시 닫기"""
    stream.start()
    yield
    stream.stop()


app = FastAPI(title="EyeCatch Bridge Service", lifespan=lifespan)


# ---- 실시간 영상 스트리밍 ----

@app.get("/live")
async def live_stream():
    """
    MJPEG 실시간 영상 스트림
    - 프론트엔드 앱이 이 URL로 접속하면 영상이 계속 흘러감
    - 예: <img src="http://브릿지IP:9000/live" />
    """
    return StreamingResponse(
        stream.generate_mjpeg(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


# ---- AI 이벤트 수신 ----

@app.post("/event")
async def receive_event(event: dict):
    """
    AI 프로세스로부터 위험 감지 이벤트를 수신한다.
    수신 즉시 메인 서버로 전달.
    """
    print(f"[브릿지] 이벤트 수신: {event.get('event_type')} - {event.get('zone_name')}")
    forward_event(event)
    return {"status": "forwarded"}


# ---- 상태 확인 ----

@app.get("/health")
async def health():
    return {"status": "bridge running", "camera": stream.is_running}


# ---- 직접 실행 ----

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_bridge:app", host=BRIDGE_HOST, port=BRIDGE_PORT, reload=True)
