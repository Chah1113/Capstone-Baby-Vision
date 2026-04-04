# EyeCatch - AI 기반 유아 안전 사고 예방 실시간 관제 시스템

> 2026학년도 1학기 기초캡스톤디자인

## 프로젝트 구조 (4파트 분리)

```
EyeCatch/
├── docs/                   # 공통 합의 문서 (API 명세, 이벤트 규격)
├── 1_frontend/             # 📱 프론트엔드 (React Native / Flutter)
├── 2_main_server/          # 🏢 메인 서버 (FastAPI)
├── 3_ai_vision/            # 🧠 AI 영상 처리 (YOLO + OpenCV)
└── 4_bridge_service/       # 🌉 브릿지 (영상 중계 + 이벤트 전달)
```

## 각 파트별 실행 방법

### 2. 메인 서버
```bash
cd 2_main_server
pip install fastapi uvicorn
uvicorn src.main:app --reload --port 8000
```

### 3. AI Vision
```bash
cd 3_ai_vision
pip install -r requirements.txt
python main_vision.py
```
> ⚠️ `weights/best.pt` (학습된 YOLO 모델)이 필요합니다.

### 4. 브릿지 서비스
```bash
cd 4_bridge_service
pip install fastapi uvicorn requests
uvicorn main_bridge:app --reload --port 9000
```

## 데이터 흐름
```
웹캠 → [3_ai_vision] → 위험 감지 → [4_bridge] → [2_main_server] → FCM 푸시 → [1_frontend]
                                        ↓
                                  영상 스트림 중계 → [1_frontend]
```

## 깃허브 규칙
- **커밋 메시지**: `feat:`, `fix:`, `docs:`, `refactor:`, `style:`
- **작업 전 Pull, 작업 후 Push**
- **Main 브랜치 직접 Push 금지** → PR로 합치기
- **각자 담당 폴더에서만 작업** (충돌 방지)

## 환경변수
- `2_main_server/.env` → `.env.example` 참고하여 생성
- `3_ai_vision/weights/best.pt` → YOLO 학습 후 배치
- Firebase 키 파일 → 깃허브 업로드 금지
