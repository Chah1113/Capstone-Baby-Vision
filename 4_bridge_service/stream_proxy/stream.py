"""
스트림 프록시
- 카메라에서 프레임을 실시간으로 읽어서
- MJPEG 스트림으로 프론트엔드(앱)에 중계
"""

import cv2
import threading
import time
from config import CAMERA_SOURCE, STREAM_FPS, STREAM_RESOLUTION, JPEG_QUALITY


class StreamProxy:
    """카메라 프레임을 읽고 MJPEG 스트림으로 제공하는 클래스"""

    def __init__(self):
        self.cap = None
        self.latest_frame = None       # 가장 최근 프레임 (bytes)
        self.is_running = False
        self.lock = threading.Lock()

    def start(self):
        """카메라를 열고 프레임 읽기를 시작한다."""
        self.cap = cv2.VideoCapture(CAMERA_SOURCE)
        if not self.cap.isOpened():
            print(f"[오류] 카메라를 열 수 없습니다: {CAMERA_SOURCE}")
            return False

        self.is_running = True
        thread = threading.Thread(target=self._capture_loop, daemon=True)
        thread.start()
        print(f"[스트림] 카메라 시작: {CAMERA_SOURCE}")
        return True

    def stop(self):
        """카메라를 닫고 프레임 읽기를 중단한다."""
        self.is_running = False
        if self.cap:
            self.cap.release()
        print("[스트림] 카메라 중지")

    def _capture_loop(self):
        """백그라운드에서 계속 프레임을 읽는 루프"""
        width, height = STREAM_RESOLUTION
        interval = 1.0 / STREAM_FPS

        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("[경고] 프레임 읽기 실패")
                time.sleep(0.1)
                continue

            # 해상도 조정
            frame = cv2.resize(frame, (width, height))

            # JPEG로 인코딩
            encode_param = [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
            _, encoded = cv2.imencode(".jpg", frame, encode_param)

            with self.lock:
                self.latest_frame = encoded.tobytes()

            time.sleep(interval)

    def get_frame(self) -> bytes:
        """가장 최근 프레임을 반환한다."""
        with self.lock:
            return self.latest_frame

    def generate_mjpeg(self):
        """
        MJPEG 스트림 제너레이터
        - FastAPI의 StreamingResponse에 넘겨서 사용
        - 프론트엔드가 /live 로 접속하면 영상이 계속 흘러감
        """
        while self.is_running:
            frame = self.get_frame()
            if frame is None:
                time.sleep(0.05)
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
            time.sleep(1.0 / STREAM_FPS)


# 전역 인스턴스 (main_bridge.py에서 import해서 사용)
stream = StreamProxy()
