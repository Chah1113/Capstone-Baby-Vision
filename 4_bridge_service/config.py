# ============================================
# EyeCatch 브릿지 서비스 설정
# 아직 미정인 항목은 기본값으로 두고,
# 확정되면 여기만 수정하면 됩니다.
# ============================================

# --- 영상 소스 (캠) ---
# 0 = 노트북 내장 웹캠
# "rtsp://..." = IP 카메라 / 홈캠
# "http://..." = MJPEG 스트림 URL
# "/path/to/video.mp4" = 테스트용 영상 파일
CAMERA_SOURCE = 0

# --- 영상 저장 ---
SAVE_DIR = "recordings"          # 저장 폴더
SAVE_FPS = 15.0                  # 저장 FPS
SAVE_RESOLUTION = (640, 480)     # 저장 해상도 (width, height)

# --- 메인 서버 (아직 미정) ---
# 확정되면 실제 주소로 변경
MAIN_SERVER_URL = "http://localhost:8000"

# --- 브릿지 서버 ---
BRIDGE_HOST = "0.0.0.0"
BRIDGE_PORT = 9000
