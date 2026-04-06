"""
카메라 리더
- 어떤 캠이든 프레임을 읽어서 통일된 포맷으로 변환
- 웹캠, RTSP, 영상 파일 모두 동일하게 처리
"""

import cv2
import time
from config import CAMERA_SOURCE, STREAM_WIDTH, STREAM_HEIGHT, STREAM_FPS


class CameraReader:
    """카메라에서 프레임을 읽는 클래스"""

    def __init__(self):
        self.cap = None
        self.is_running = False

    def open(self) -> bool:
        """카메라를 연다."""
        self.cap = cv2.VideoCapture(CAMERA_SOURCE)
        if not self.cap.isOpened():
            print(f"[오류] 카메라를 열 수 없습니다: {CAMERA_SOURCE}")
            return False

        self.is_running = True
        print(f"[카메라] 연결 성공: {CAMERA_SOURCE}")
        print(f"[카메라] 출력 포맷: {STREAM_WIDTH}x{STREAM_HEIGHT} @ {STREAM_FPS}fps")
        return True

    def close(self):
        """카메라를 닫는다."""
        self.is_running = False
        if self.cap:
            self.cap.release()
        print("[카메라] 연결 종료")

    def read_frame(self):
        """
        프레임 하나를 읽어서 해상도를 통일한다.
        실패 시 None 반환.
        """
        if not self.cap or not self.is_running:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        # 해상도 통일 (캠 종류 무관)
        frame = cv2.resize(frame, (STREAM_WIDTH, STREAM_HEIGHT))
        return frame

    def reconnect(self, max_retries: int = 5, wait_sec: float = 3.0) -> bool:
        """
        카메라 연결이 끊겼을 때 재연결을 시도한다.

        Args:
            max_retries: 최대 재시도 횟수
            wait_sec: 재시도 간 대기 시간(초)
        """
        print("[카메라] 연결 끊김. 재연결 시도 중...")
        self.close()

        for attempt in range(1, max_retries + 1):
            print(f"[카메라] 재연결 시도 {attempt}/{max_retries}")
            time.sleep(wait_sec)

            if self.open():
                print("[카메라] 재연결 성공!")
                return True

        print("[카메라] 재연결 실패. 모든 시도 소진.")
        return False
