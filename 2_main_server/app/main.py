from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.base import engine, Base
from routers import users, cameras, danger_zones, alerts

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# 👈 2. CORS 미들웨어 설정 (여기부터)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 모든 주소에서의 접근을 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],     # POST, GET, OPTIONS 등 모든 통신 방식 허용
    allow_headers=["*"],     # 모든 헤더 허용
)
# (여기까지 추가) 👉

# 라우터 등록
app.include_router(users.router)
app.include_router(cameras.router)
app.include_router(danger_zones.router)
app.include_router(alerts.router)