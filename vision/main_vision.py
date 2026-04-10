"""
EyeCatch AI Vision 메인 실행 스크립트
- API에서 카메라 목록을 주기적으로 확인 → 추가/제거된 카메라에 스레드 동적 관리
- 화면 출력은 메인 스레드에서만 처리 (cv2 멀티스레드 안전)
"""

import cv2
import time
import os
import queue
import threading
import requests
from models.detector import PersonDetector
from core.zone_checker import ZoneManager
from utils.drawing import draw_detections, draw_zones, draw_warning_banner


# ========== 설정 ==========
MODEL_PATH           = os.getenv("MODEL_PATH", "yolov8n.pt")  # 기본: yolov8n 자동 다운로드 / 실제: weights/best.pt
MAIN_SERVER_URL      = os.getenv("MAIN_SERVER_URL", "http://api:8000")
MEDIAMTX_HOST        = os.getenv("MEDIAMTX_HOST", "mediamtx")
ALERT_COOLDOWN       = 5   # 같은 구역 재알림 대기 시간(초)
CAMERA_POLL_INTERVAL = 30  # 카메라 목록 갱신 주기(초)
SHOW_DISPLAY         = os.getenv("SHOW_DISPLAY", "false").lower() == "true"
# ==========================


def fetch_all_cameras() -> list:
    """API에서 활성 카메라 전체 목록을 가져오고 stream_url을 내부 호스트로 변환한다."""
    try:
        response = requests.get(f"{MAIN_SERVER_URL}/cameras/internal", timeout=5)
        response.raise_for_status()
        cameras = response.json()
        server_host = os.getenv("SERVER_HOST", "localhost")
        for cam in cameras:
            cam["stream_url"] = cam["stream_url"].replace(
                f"://{server_host}:", f"://{MEDIAMTX_HOST}:"
            )
        return cameras
    except Exception as e:
        print(f"[오류] 카메라 목록 조회 실패: {e}")
        return []


def fetch_zones_for_camera(camera_id: int) -> list:
    """API에서 특정 카메라의 위험구역을 가져온다."""
    try:
        response = requests.get(f"{MAIN_SERVER_URL}/danger-zones/internal/{camera_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[경고] 구역 정보 로드 실패 (camera_id={camera_id}): {e}")
        return []


def send_event_to_api(event: dict):
    """API 서버로 위험 감지 이벤트를 전송한다."""
    try:
        requests.post(f"{MAIN_SERVER_URL}/events", json=event, timeout=3)
    except Exception as e:
        print(f"[경고] 이벤트 전송 실패: {e}")


def run_camera(camera: dict, stop_event: threading.Event, frame_queue: queue.Queue):
    """단일 카메라 감지 루프 — 스레드로 실행된다.
    - stop_event가 set되면 종료
    - SHOW_DISPLAY=true 시 처리된 프레임을 frame_queue에 넣어 메인 스레드가 표시
    """
    camera_id   = camera["id"]
    camera_name = camera["name"]
    rtsp_url    = camera["stream_url"]

    camera_zones = fetch_zones_for_camera(camera_id)
    zone_manager = ZoneManager()
    zone_manager.load_zones(camera_zones)
    print(f"[{camera_name}] 위험구역 {len(zone_manager.zones)}개 로드")

    detector = PersonDetector(model_path=MODEL_PATH)

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print(f"[{camera_name}] RTSP 연결 실패: {rtsp_url}")
        return

    frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[{camera_name}] 감지 시작 ({frame_width}x{frame_height})")

    last_alert_time = {}

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print(f"[{camera_name}] 스트림 끊김")
            break

        detections = detector.detect(frame)
        warning_message = None

        for det in detections:
            if det["class_name"] != "baby":
                continue

            cx, cy = det["center"]
            intruded_zones = zone_manager.check_intrusion(cx, cy, frame_width, frame_height)

            for zone in intruded_zones:
                now = time.time()
                if now - last_alert_time.get(zone.zone_id, 0) > ALERT_COOLDOWN:
                    last_alert_time[zone.zone_id] = now
                    warning_message = f"WARNING: Baby in [{zone.name}]!"

                    send_event_to_api({
                        "camera_id": camera_id,
                        "event_type": "ZONE_INTRUSION",
                        "zone_id": zone.zone_id,
                        "zone_name": zone.name,
                        "confidence": det["confidence"],
                        "bbox": list(det["bbox"]),
                    })
                    print(f"[{camera_name}] {warning_message}")

        # 화면 출력용 프레임 준비 — 그리기만 하고 imshow는 메인 스레드에서
        if SHOW_DISPLAY:
            draw_detections(frame, detections)
            if zone_manager.zones:
                draw_zones(frame, camera_zones, frame_width, frame_height)
            if warning_message:
                draw_warning_banner(frame, warning_message)
            # maxsize=1 큐: 최신 프레임만 유지 (가득 차 있으면 버림)
            try:
                frame_queue.put_nowait((camera_name, frame))
            except queue.Full:
                pass

    cap.release()
    print(f"[{camera_name}] 스레드 종료")


def watch_cameras(running: dict, lock: threading.Lock):
    """카메라 목록을 주기적으로 확인하고 스레드를 동적으로 관리한다."""
    while True:
        cameras = fetch_all_cameras()
        active_ids = {c["id"]: c for c in cameras}

        with lock:
            # 새로 추가된 카메라 → 스레드 시작
            for camera_id, camera in active_ids.items():
                if camera_id not in running:
                    stop_event = threading.Event()
                    fq = queue.Queue(maxsize=1)
                    t = threading.Thread(
                        target=run_camera,
                        args=(camera, stop_event, fq),
                        daemon=True,
                    )
                    t.start()
                    running[camera_id] = (t, stop_event, fq)
                    print(f"[추가] [{camera['name']}] 스레드 시작")

            # 비활성/삭제된 카메라 → 스레드 종료
            for camera_id in list(running.keys()):
                if camera_id not in active_ids:
                    t, stop_event, _ = running.pop(camera_id)
                    stop_event.set()
                    t.join(timeout=5)  # 최대 5초 대기 후 리소스 정리 보장
                    print(f"[제거] camera_id={camera_id} 스레드 종료")

        time.sleep(CAMERA_POLL_INTERVAL)


def main():
    # camera_id → (thread, stop_event, frame_queue)
    running: dict[int, tuple[threading.Thread, threading.Event, queue.Queue]] = {}
    lock = threading.Lock()

    print(f"[시작] 카메라 감지 시작 (갱신 주기: {CAMERA_POLL_INTERVAL}초)")

    # 카메라 감시는 별도 스레드에서 실행
    watcher = threading.Thread(target=watch_cameras, args=(running, lock), daemon=True)
    watcher.start()

    if SHOW_DISPLAY:
        # 메인 스레드에서만 cv2 화면 출력 (스레드 안전)
        print("[정보] 화면 출력 모드 — q 키로 종료")
        while True:
            with lock:
                queues = [(cid, data[2]) for cid, data in running.items()]

            for camera_id, fq in queues:
                try:
                    camera_name, frame = fq.get_nowait()
                    cv2.imshow(f"EyeCatch - {camera_name}", frame)
                except queue.Empty:
                    pass

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()
    else:
        # 서버 배포 모드 — watcher 스레드가 끝날 때까지 대기
        watcher.join()

    print("[종료] AI Vision 종료")


if __name__ == "__main__":
    main()
