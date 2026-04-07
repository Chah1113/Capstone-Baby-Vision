#!/bin/bash

echo "=========================================="
echo "  EyeCatch Main Server Starting..."
echo "=========================================="

# MediaMTX 백그라운드 실행
echo "[1/2] Starting MediaMTX (RTSP Server)..."
mediamtx &
MEDIAMTX_PID=$!

# 잠시 대기 (MediaMTX 초기화)
sleep 2

# FastAPI 실행
echo "[2/2] Starting FastAPI Server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
FASTAPI_PID=$!

echo "=========================================="
echo "  ✅ Main Server Ready!"
echo "  - FastAPI: http://0.0.0.0:8000"
echo "  - RTSP: rtsp://0.0.0.0:8554/stream"
echo "=========================================="

# 두 프로세스 모니터링
wait $FASTAPI_PID $MEDIAMTX_PID
