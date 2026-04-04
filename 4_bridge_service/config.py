# ============================================
# EyeCatch 브릿지 서비스 설정
# 확정되지 않은 항목은 기본값으로 두고,
# 나중에 여기만 수정하면 됩니다.
# ============================================

# --- 영상 소스 (캠) ---
# 0 = 노트북 내장 웹캠
# "rtsp://..." = IP 카메라 / 홈캠
# "http://..." = MJPEG 스트림 URL
# "/path/to/video.mp4" = 테스트용 영상 파일
CAMERA_SOURCE = 0

# --- 스트리밍 설정 ---
STREAM_FPS = 15                  # 프론트에 보낼 FPS
STREAM_RESOLUTION = (640, 480)   # 스트림 해상도 (width, height)
JPEG_QUALITY = 70                # MJPEG 압축 품질 (1~100, 낮을수록 가벼움)

# --- 메인 서버 (아직 미정) ---
# 확정되면 실제 주소로 변경
MAIN_SERVER_URL = "http://localhost:8000"
EVENT_ENDPOINT = "/api/alerts/event"

# --- 브릿지 서버 ---
BRIDGE_HOST = "0.0.0.0"
BRIDGE_PORT = 9000
