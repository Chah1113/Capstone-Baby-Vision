"""
EyeCatch 메인 서버 진입점
- 프론트엔드 앱과 REST API 통신
- 브릿지로부터 위험 감지 이벤트 수신
- FCM 푸시 알림 전송
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import zones, alerts, users, stream

app = FastAPI(
    title="EyeCatch Main Server",
    description="AI 기반 유아 안전 관제 시스템 메인 서버",
    version="0.1.0",
)

# CORS 설정 (모바일 앱 & 개발 환경 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 특정 도메인으로 제한할 것
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(zones.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(stream.router, prefix="/api")


@app.get("/")
async def root():
    """서버 상태 확인"""
    return {"service": "EyeCatch", "status": "running"}


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}
