# 향후 구현 사항

## 1. 스냅샷 저장

위험 감지 시 해당 프레임 이미지를 파일로 저장하는 기능.

**구현 위치:** `vision/main_vision.py`

**구현 내용:**
- 침범 감지 시 `cv2.imwrite()`로 프레임 저장
- 저장 경로를 `POST /events` payload의 `snapshot_path` 필드에 포함
- 저장된 이미지를 Flutter에서 조회할 수 있도록 API에 정적 파일 서빙 추가

**관련 필드:** `api/db/models.py` — `DetectionEvent.snapshot_path`

---

## 2. 멀티카메라 동시 처리

현재는 vision 컨테이너 1개 = 카메라 1대. 사용자가 늘어 카메라가 여러 대가 되면 모든 카메라를 동시에 분석해야 한다.

**방안 A — 컨테이너 스케일 아웃 (단순):**
```bash
# 카메라별로 CAMERA_ID, RTSP_URL을 다르게 설정한 vision 컨테이너를 각각 실행
docker compose up --scale vision=N
```
단, 각 컨테이너가 다른 환경변수를 가져야 하므로 docker-compose 설정 분리 필요.

**방안 B — vision 내부 멀티스레드 (복잡):**
- 시작 시 `GET /cameras/internal` 로 전체 카메라 목록 조회
- 카메라별로 스레드를 생성해 RTSP 스트림 병렬 처리
- 각 스레드가 해당 `camera_id`를 이벤트에 포함해 전송

**관련 파일:** `vision/main_vision.py`, `docker-compose.yml`
