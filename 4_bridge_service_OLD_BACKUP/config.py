# ============================================
# EyeCatch 브릿지 설정
# 캠에서 읽은 영상을 MediaMTX(RTSP)로 push
# 확정되면 여기만 수정하면 됩니다.
# ============================================

# --- 영상 소스 (캠) ---
# 0 = 노트북 내장 웹캠
# "rtsp://..." = IP 카메라 / 홈캠 / 라즈베리파이
# "/path/to/video.mp4" = 테스트용 영상 파일
CAMERA_SOURCE = 0

# --- 영상 포맷 (캠 종류 무관하게 통일) ---
STREAM_WIDTH = 640
STREAM_HEIGHT = 480
STREAM_FPS = 15

# --- MediaMTX 서버 (docker-compose의 mediamtx) ---
# 같은 컴퓨터에서 도커 돌리면 localhost
# 다른 컴퓨터면 해당 IP로 변경
MEDIAMTX_HOST = "localhost"
MEDIAMTX_RTSP_PORT = 8554

# --- 메인 서버 API ---
MAIN_SERVER_URL = "http://localhost:8000"
