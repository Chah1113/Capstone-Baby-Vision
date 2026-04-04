"""
스트림 프록시 서버
- AI가 처리한 실시간 영상을 프론트엔드로 중계
- MJPEG 스트리밍 방식 (기본)

TODO: 브릿지 담당자가 구현
- WebRTC 또는 RTSP로 변경 가능
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import asyncio

app = FastAPI(title="EyeCatch Stream Proxy")

# TODO: AI 프로세스로부터 프레임을 받는 방식 구현
# 방법 1) 공유 메모리 / 방법 2) 소켓 / 방법 3) Redis


async def generate_mjpeg():
    """
    MJPEG 스트림 제너레이터 (스켈레톤)
    - 실제로는 AI에서 처리된 프레임을 받아서 전달
    """
    # TODO: AI 프로세스에서 프레임 수신 로직 구현
    while True:
        # placeholder: 실제 프레임 대신 빈 프레임
        frame = cv2.imencode(".jpg", cv2.waitKey(1))[1].tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )
        await asyncio.sleep(1 / 30)  # ~30fps


@app.get("/live")
async def live_stream():
    """실시간 MJPEG 스트림 엔드포인트"""
    return StreamingResponse(
        generate_mjpeg(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.get("/health")
async def health():
    return {"status": "stream_proxy running"}
