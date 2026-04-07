"""
RTSP 스트림 푸셔
- OpenCV로 읽은 프레임을 FFmpeg 프로세스를 통해 MediaMTX로 push
- MediaMTX가 RTSP 서버 역할을 하므로, 앱과 AI가 여기서 영상을 가져감
"""

import subprocess
import sys
from config import STREAM_WIDTH, STREAM_HEIGHT, STREAM_FPS


class RtspPusher:
    """FFmpeg subprocess를 이용해 RTSP 스트림을 push하는 클래스"""

    def __init__(self, rtsp_url: str):
        """
        Args:
            rtsp_url: MediaMTX의 RTSP 주소 (예: rtsp://localhost:8554/abc-123)
        """
        self.rtsp_url = rtsp_url
        self.process = None

    def start(self) -> bool:
        """FFmpeg 프로세스를 시작한다."""
        command = [
            "ffmpeg",
            "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", f"{STREAM_WIDTH}x{STREAM_HEIGHT}",
            "-r", str(STREAM_FPS),
            "-i", "-",                      # stdin에서 프레임 읽기
            "-c:v", "libx264",
            "-preset", "ultrafast",         # 최소 지연
            "-tune", "zerolatency",         # 실시간 스트리밍 최적화
            "-f", "rtsp",
            "-rtsp_transport", "tcp",
            self.rtsp_url,
        ]

        try:
            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(f"[스트림] RTSP push 시작 → {self.rtsp_url}")
            return True
        except FileNotFoundError:
            print("[오류] FFmpeg이 설치되어 있지 않습니다.")
            print("[안내] 설치 방법: https://ffmpeg.org/download.html")
            print("[안내] Windows: choco install ffmpeg 또는 winget install ffmpeg")
            return False
        except Exception as e:
            print(f"[오류] FFmpeg 시작 실패: {e}")
            return False

    def push_frame(self, frame) -> bool:
        """
        한 프레임을 RTSP 스트림으로 보낸다.

        Args:
            frame: OpenCV BGR 프레임 (numpy array, STREAM_WIDTH x STREAM_HEIGHT)
        """
        if not self.process or self.process.poll() is not None:
            return False

        try:
            self.process.stdin.write(frame.tobytes())
            return True
        except BrokenPipeError:
            print("[스트림] FFmpeg 연결 끊김")
            return False

    def stop(self):
        """FFmpeg 프로세스를 종료한다."""
        if self.process:
            self.process.stdin.close()
            self.process.wait()
            self.process = None
        print("[스트림] RTSP push 종료")
