# EyeCatch 시스템 아키텍처

> 작성일: 2026-04-16 / 현재 코드 기준

---

## 전체 구조

```
Flutter App
    │
    │ REST API (HTTP:8000)
    ▼
┌─────────┐     내부 네트워크      ┌──────────────┐
│   API   │ ◄──────────────────► │    Vision    │
│(FastAPI)│                      │ (YOLO+OpenCV)│
└────┬────┘                      └──────┬───────┘
     │                                   │
     │ SQL                        RTSP 구독
     ▼                                   │
┌──────────┐      RTSP 송출       ┌──────▼────────┐
│PostgreSQL│              ┌──────►│  MediaMTX    │
└──────────┘              │       │(RTSP/HLS/WRC)│
                    카메라 앱      └──────────────┘
```

---

## 서비스별 상세
                                                                  
### 1. API 서버 (`api/`)

**역할:** 사용자 인증, 카메라 관리, 위험구역 관리, 알림 조회

**기술:** FastAPI (Python), SQLAlchemy async, PostgreSQL

**포트:** 8000

#### 엔드포인트 목록

| 메서드 | 경로 | 설명 | 인증 |
|--------|------|------|------|
| POST | `/users/register` | 회원가입 | 없음 |
| POST | `/users/login` | 로그인 (access + refresh 토큰 발급) | 없음 |
| POST | `/users/refresh` | 토큰 갱신 | 없음 |
| GET | `/users/me` | 내 정보 조회 | Bearer |
| PATCH | `/users/me` | 이름 수정 | Bearer |
| PATCH | `/users/me/password` | 비밀번호 변경 | Bearer |
| DELETE | `/users/me` | 회원 탈퇴 | Bearer |
| POST | `/cameras` | 카메라 등록 (UUID 발급) | Bearer |
| GET | `/cameras` | 내 카메라 목록 | Bearer |
| GET | `/cameras/{id}` | 카메라 상세 | Bearer |
| PATCH | `/cameras/{id}` | is_active 수정 | Bearer |
| DELETE | `/cameras/{id}` | 카메라 삭제 | Bearer |
| GET | `/cameras/internal` | 전체 활성 카메라 (Vision 전용) | 없음 |
| PATCH | `/cameras/internal/{id}/status` | 연결 상태 갱신 (Vision 전용) | 없음 |
| POST | `/danger-zones` | 위험구역 생성 | Bearer |
| GET | `/danger-zones/{camera_id}` | 카메라별 위험구역 조회 | Bearer |
| PUT | `/danger-zones/{zone_id}` | 위험구역 수정 | Bearer |
| DELETE | `/danger-zones/{zone_id}` | 위험구역 삭제 | Bearer |
| GET | `/danger-zones/internal/{camera_id}` | 위험구역 조회 (Vision 전용) | 없음 |
| POST | `/events` | 감지 이벤트 수신 (Vision 전용) | 없음 |
| GET | `/alerts` | 알림 목록 (페이징) | Bearer |
| PATCH | `/alerts/{id}/read` | 알림 읽음 처리 | Bearer |

#### 인증 구조

- JWT HS256, access token 1시간 / refresh token 30일
- `Authorization: Bearer <token>` 헤더

#### 카메라 UUID 발급 흐름

카메라 등록 시 서버가 UUID를 직접 생성해 RTSP URL에 포함시킨다.

```
POST /cameras → stream_url = rtsp://{SERVER_HOST}:8554/{uuid4()}
```

카메라 앱은 이 `stream_url`로 MediaMTX에 송출한다.

---

### 2. Vision 서비스 (`vision/`)

**역할:** RTSP 스트림 수신 → YOLO 감지 → 위험구역 침범 판정 → API 이벤트 전송

**기술:** Python, Ultralytics YOLOv8, OpenCV, Shapely

#### 동작 흐름

```
1. 시작 시 GET /cameras/internal 호출 → 활성 카메라 목록 확보
2. 카메라별로 스레드 생성
3. 각 스레드:
   a. GET /danger-zones/internal/{camera_id} → 위험구역 로드
   b. cv2.VideoCapture(rtsp_url) → RTSP 연결
   c. 프레임마다 YOLO 추론
   d. 바운딩 박스가 위험구역 다각형과 겹치면 이벤트 전송
   e. 5초 쿨다운으로 중복 전송 방지
4. 30초마다 카메라 목록 갱신 (추가/삭제된 카메라 반영)
60초마다 위험구역 갱신
```

#### 위험 감지 판정

- 바운딩 박스(픽셀) → 정규화 좌표(0.0~1.0) 변환
- Shapely `Polygon.intersects(box)` 로 겹침 판단
- 단일 점이 아닌 **박스 일부라도 겹치면** 감지

#### 내부 호스트 변환

DB에 저장된 `stream_url`은 외부 IP 기준이므로, Vision은 Docker 내부 호스트명으로 변환해 연결한다.

```python
rtsp://211.x.x.x:8554/{uuid}  →  rtsp://mediamtx:8554/{uuid}
```

#### 환경변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MODEL_PATH` | `yolov8n.pt` | YOLO 모델 파일 경로 |
| `MAIN_SERVER_URL` | `http://api:8000` | API 서버 주소 |
| `MEDIAMTX_HOST` | `mediamtx` | MediaMTX 내부 호스트명 |
| `SHOW_DISPLAY` | `false` | OpenCV 화면 출력 (로컬 테스트용) |

---

### 3. MediaMTX (`mediamtx/`)

**역할:** RTSP 스트림 중계 서버. 카메라 앱에서 영상을 받아 Vision 서비스가 구독할 수 있도록 유지.

**기술:** bluenviron/mediamtx (Go)

#### 지원 프로토콜

| 프로토콜 | 포트 | 용도 |
|---------|------|------|
| RTSP | 8554 | 카메라 앱 송출 / Vision 구독 |
| HLS | 8888 | `http://{host}:8888/{uuid}/index.m3u8` |
| WebRTC | 8889 | `http://{host}:8889/{uuid}` (브라우저 확인용) |
| MediaMTX API | 9997 | 활성 스트림 목록 확인 |

#### 스트림 경로 확인

```bash
curl http://localhost:9997/v3/paths/list
```

#### 주요 설정

```yaml
# mediamtx/mediamtx.yml
paths:
  all:
    source: publisher   # 누구든 아무 경로로 publish 가능
```

> 현재 DB UUID 검증 없음. 아무 경로로 송출해도 수락됨.

---

### 4. 데이터베이스 (`PostgreSQL`)

**포트:** 5432 (외부), Docker 내부 `db:5432`

#### 테이블 구조

```
users
├── id (PK)
├── email (unique)
├── password_hash
└── name

cameras
├── id (PK)
├── user_id (FK → users)
├── name
├── stream_url          ← rtsp://{host}:8554/{uuid} 형태
├── is_active
├── is_connected
└── updated_at

danger_zones
├── id (PK)
├── camera_id (FK → cameras)
├── label
└── zone_points (JSONB) ← [[x, y], ...] 정규화 좌표 (0.0~1.0)

detection_events
├── id (PK)
├── camera_id (FK → cameras)
├── event_type
├── zone_id             ← DangerZone 참조 (FK 없음, 삭제 후에도 이력 보존)
├── zone_name
├── confidence
├── bbox (JSONB)        ← [x1, y1, x2, y2]
└── detected_at

alerts
├── id (PK)
├── user_id (FK → users)
├── detection_id (FK → detection_events, SET NULL on delete)
├── message
├── is_read
└── sent_at
```

#### cascade 규칙

- user 삭제 → cameras, alerts CASCADE 삭제
- camera 삭제 → danger_zones, detection_events CASCADE 삭제
- detection_event 삭제 → alerts.detection_id SET NULL (알림 이력 보존)

---

## 이벤트 전송 흐름 (감지 → 알림)

```
Vision 감지
    │
    │ POST /events
    │ {camera_id, event_type, zone_id, zone_name, confidence, bbox}
    ▼
API /events
    ├── detection_events 저장
    └── alerts 생성 → Flutter 앱 폴링으로 수신
```

> 현재 실시간 푸시 없음. Flutter 앱이 GET /alerts 폴링 방식.
> FCM 푸시 알림은 미구현 상태.

---

## Docker Compose 서비스 구성

| 서비스 | 이미지 | 포트 |
|--------|--------|------|
| `db` | postgres:16 | 5432 |
| `api` | ./api (빌드) | 8000 |
| `vision` | ./vision (빌드) | - |
| `mediamtx` | bluenviron/mediamtx | 8554, 8888, 8889, 8189, 9997 |
| `pgadmin` | dpage/pgadmin4 | 5050 |

---

## 알려진 제한사항

- `/internal` 엔드포인트에 별도 인증 없음 (Docker 내부망 의존)
- CORS `allow_origins=["*"]` + `allow_credentials=True` 조합 비호환
- refresh 토큰 DB 저장 안 함 (로그아웃 후에도 30일간 유효)
- FCM 푸시 알림 미구현
