# ============================================
# EyeCatch 카메라 설정
# 제출 시 여기만 수정하면 됩니다
# ============================================
import os

# ===== 카메라 소스 (제출 시 변경) =====
# 0 = 노트북 내장 웹캠
# "rtsp://192.168.0.100/stream" = IP 카메라 / 홈캠
# "/dev/video0" = 라즈베리파이
CAMERA_SOURCE = int(os.getenv("CAMERA_SOURCE", "0"))

# ===== 영상 포맷 =====
STREAM_WIDTH = 640
STREAM_HEIGHT = 480
STREAM_FPS = 15

# ===== MediaMTX 주소 (도커 내부) =====
MEDIAMTX_RTSP_URL = "rtsp://localhost:8554/stream"
