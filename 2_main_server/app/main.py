from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.base import engine, Base
from routers import users, cameras, danger_zones, alerts

# ===== Bridge Service 추가 =====
from bridge.bridge_service import BridgeService
from config import (
    CAMERA_SOURCE,
    MEDIAMTX_RTSP_URL,
    STREAM_WIDTH,
    STREAM_HEIGHT,
    STREAM_FPS
)

# ===== 전역 변수 =====
bridge_service: BridgeService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 시작/종료 시 실행"""
    global bridge_service
    
    # 시작 시
    print("\n" + "="*50)
    print("  EyeCatch Main Server - FastAPI")
    print("="*50)
    
    # DB 초기화
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[DB] 데이터베이스 초기화 완료")
    
    # Bridge Service 시작
    print("\n[Bridge] 카메라 스트리밍 시작...")
    bridge_service = BridgeService(
        camera_source=CAMERA_SOURCE,
        rtsp_url=MEDIAMTX_RTSP_URL,
        width=STREAM_WIDTH,
        height=STREAM_HEIGHT,
        fps=STREAM_FPS
    )
    
    if bridge_service.start():
        print("[Bridge] ✅ 카메라 스트리밍 준비 완료")
    else:
        print("[Bridge] ⚠️  카메라 시작 실패 (계속 진행)")
    
    print("\n" + "="*50)
    print("  ✅ Main Server Ready!")
    print(f"  - API: http://0.0.0.0:8000")
    print(f"  - RTSP: {MEDIAMTX_RTSP_URL}")
    print(f"  - Camera: {CAMERA_SOURCE}")
    print("="*50 + "\n")
    
    yield  # 서버 실행
    
    # 종료 시
    print("\n[종료] Main Server 종료 중...")
    if bridge_service:
        bridge_service.stop()
    print("[종료] 완료\n")


app = FastAPI(lifespan=lifespan)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(users.router)
app.include_router(cameras.router)
app.include_router(danger_zones.router)
app.include_router(alerts.router)


# ===== Bridge 상태 확인 엔드포인트 =====
@app.get("/bridge/status")
def get_bridge_status():
    """Bridge Service 상태 확인"""
    if not bridge_service:
        return {
            "running": False,
            "message": "Bridge service not initialized"
        }
    
    return {
        "running": bridge_service.is_running(),
        "camera_source": CAMERA_SOURCE,
        "rtsp_url": MEDIAMTX_RTSP_URL,
        "resolution": f"{STREAM_WIDTH}x{STREAM_HEIGHT}",
        "fps": STREAM_FPS
    }


@app.get("/")
def root():
    """서버 상태 확인"""
    return {
        "service": "EyeCatch Main Server",
        "status": "running",
        "bridge_running": bridge_service.is_running() if bridge_service else False
    }
