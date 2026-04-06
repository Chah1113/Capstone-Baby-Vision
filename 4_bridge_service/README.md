# 4_bridge_service - 영상 스트리밍 브릿지

웹캠(또는 IP캠)에서 OpenCV로 영상을 읽어서 메인 서버의 MediaMTX(RTSP)로 push합니다.
앱과 AI는 MediaMTX에서 영상을 가져갑니다.

## 흐름

```
웹캠 → [이 코드: OpenCV] → MediaMTX(RTSP) → 앱 (실시간 시청)
                                            → AI (YOLO 분석)
```

## 사전 준비

1. **Docker Desktop** 설치 및 실행
2. **FFmpeg** 설치 (`choco install ffmpeg` 또는 https://ffmpeg.org)
3. 메인 서버 실행: `cd 2_main_server && docker compose up`
4. 파이썬 라이브러리: `pip install -r requirements.txt`

## 실행

```bash
cd 4_bridge_service
python main.py
```

실행하면 이메일/비밀번호 입력 → 카메라 등록 → 영상 스트리밍 자동 시작

## 캠 변경

`config.py`에서 `CAMERA_SOURCE`만 수정:

```python
CAMERA_SOURCE = 0                          # 노트북 웹캠
CAMERA_SOURCE = "rtsp://192.168.0.5/live"  # IP캠 / 라즈베리파이
```
