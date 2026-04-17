"""
MJPEG HTTP 스트리밍 서버
- /            : 전체 카메라 모니터 페이지
- /stream/<name> : 특정 카메라 MJPEG 스트림
"""

import threading
import time
import cv2
from flask import Flask, Response

app = Flask(__name__)

_latest_frames: dict[str, bytes] = {}
_lock = threading.Lock()


def update_frame(camera_name: str, frame) -> None:
    """카메라 스레드에서 호출 — 최신 어노테이션 프레임을 JPEG로 저장한다."""
    _, jpeg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
    with _lock:
        _latest_frames[camera_name] = jpeg.tobytes()


def _generate(camera_name: str):
    """MJPEG 스트림 제너레이터"""
    while True:
        with _lock:
            jpeg = _latest_frames.get(camera_name)
        if jpeg:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"
        else:
            time.sleep(0.05)


@app.route("/stream/<camera_name>")
def stream(camera_name: str):
    return Response(
        _generate(camera_name),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/")
def index():
    with _lock:
        names = list(_latest_frames.keys())

    cards = "".join(
        f"""
        <div class="card">
          <h3>{name}</h3>
          <img src="/stream/{name}">
        </div>"""
        for name in names
    )

    placeholder = "<p class='placeholder'>연결된 카메라가 없습니다.</p>" if not names else ""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="10">
  <title>EyeCatch Vision Monitor</title>
  <style>
    body {{ font-family: sans-serif; background: #111; color: #eee; margin: 0; padding: 20px; }}
    h1   {{ margin-bottom: 20px; }}
    .grid {{ display: flex; flex-wrap: wrap; gap: 16px; }}
    .card {{ background: #222; border-radius: 8px; padding: 12px; }}
    .card h3 {{ margin: 0 0 8px; font-size: 14px; color: #aaa; }}
    .card img {{ display: block; max-width: 640px; width: 100%; border-radius: 4px; }}
    .placeholder {{ color: #666; }}
  </style>
</head>
<body>
  <h1>EyeCatch Vision Monitor</h1>
  <div class="grid">{cards}{placeholder}</div>
</body>
</html>"""


def start(port: int = 8090) -> None:
    """백그라운드 스레드에서 Flask 서버를 시작한다."""
    t = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=port, threaded=True),
        daemon=True,
    )
    t.start()
    print(f"[스트림] 모니터 서버 시작: http://0.0.0.0:{port}")
