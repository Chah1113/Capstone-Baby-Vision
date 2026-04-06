"""
EyeCatch 브릿지 메인 실행 스크립트
- 메인 서버에 카메라 등록 → RTSP 주소 받기
- 웹캠에서 OpenCV로 프레임 읽기
- MediaMTX로 RTSP push (앱/AI가 여기서 영상을 가져감)

실행: python main.py
"""

import cv2
import time
import requests
from camera import CameraReader
from rtsp_pusher import RtspPusher
from config import (
    MAIN_SERVER_URL,
    MEDIAMTX_HOST,
    MEDIAMTX_RTSP_PORT,
    STREAM_FPS,
)


def register_camera(token: str, camera_name: str = "bridge-cam") -> str:
    """
    메인 서버에 카메라를 등록하고 RTSP 주소를 받아온다.

    Args:
        token: 로그인 후 받은 JWT 토큰
        camera_name: 카메라 이름

    Returns:
        RTSP 스트림 URL (예: rtsp://localhost:8554/abc-123)
    """
    url = f"{MAIN_SERVER_URL}/cameras"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {"name": camera_name}

    try:
        response = requests.post(url, json=body, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            rtsp_url = data["stream_url"]
            print(f"[서버] 카메라 등록 완료: {data['name']} (ID: {data['id']})")
            print(f"[서버] RTSP 주소: {rtsp_url}")
            return rtsp_url
        else:
            print(f"[서버] 카메라 등록 실패: {response.status_code} - {response.text}")
            return ""
    except requests.ConnectionError:
        print(f"[서버] 연결 실패: {url}")
        print("[안내] docker compose up 으로 서버가 켜져있는지 확인하세요.")
        return ""


def login(email: str, password: str) -> str:
    """
    메인 서버에 로그인하고 JWT 토큰을 받아온다.

    Returns:
        access_token 문자열. 실패 시 빈 문자열.
    """
    url = f"{MAIN_SERVER_URL}/users/login"
    body = {"email": email, "password": password}

    try:
        response = requests.post(url, json=body, timeout=10)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"[서버] 로그인 성공")
            return token
        else:
            print(f"[서버] 로그인 실패: {response.text}")
            return ""
    except requests.ConnectionError:
        print(f"[서버] 연결 실패: {url}")
        return ""


def main():
    print("=" * 50)
    print("  EyeCatch Bridge - 영상 스트리밍")
    print("=" * 50)

    # 1단계: 서버 로그인
    print("\n[1/4] 서버 로그인")
    email = input("  이메일: ")
    password = input("  비밀번호: ")
    token = login(email, password)
    if not token:
        print("[중단] 로그인 실패. 종료합니다.")
        return

    # 2단계: 카메라 등록 → RTSP 주소 받기
    print("\n[2/4] 카메라 등록")
    rtsp_url = register_camera(token)
    if not rtsp_url:
        print("[중단] 카메라 등록 실패. 종료합니다.")
        return

    # docker-compose의 mediamtx는 내부에서 localhost로 접근 가능
    # 서버의 cameras.py가 SERVER_HOST 기준으로 URL을 만들어주므로 그대로 사용
    print(f"[정보] 영상 push 대상: {rtsp_url}")

    # 3단계: 카메라 열기
    print("\n[3/4] 카메라 연결")
    camera = CameraReader()
    if not camera.open():
        print("[중단] 카메라 연결 실패. 종료합니다.")
        return

    # 4단계: RTSP push 시작
    print("\n[4/4] 스트리밍 시작")
    pusher = RtspPusher(rtsp_url)
    if not pusher.start():
        camera.close()
        print("[중단] RTSP push 실패. FFmpeg 설치를 확인하세요.")
        return

    interval = 1.0 / STREAM_FPS
    frame_count = 0
    fail_count = 0

    print(f"\n[실행 중] {STREAM_FPS}fps로 MediaMTX에 영상 전송 중...")
    print("[안내] q 키를 누르면 종료합니다.")
    print(f"[안내] 앱/AI에서 이 주소로 영상 수신 가능: {rtsp_url}\n")

    try:
        while True:
            frame = camera.read_frame()

            # 프레임 읽기 실패 → 재연결 시도
            if frame is None:
                fail_count += 1
                if fail_count >= 30:
                    if not camera.reconnect():
                        print("[중단] 카메라 재연결 실패. 종료합니다.")
                        break
                    fail_count = 0
                continue

            fail_count = 0
            frame_count += 1

            # MediaMTX로 push
            if not pusher.push_frame(frame):
                print("[경고] 스트림 push 실패. 재시작 시도...")
                pusher.stop()
                time.sleep(1)
                if not pusher.start():
                    print("[중단] 스트림 재시작 실패. 종료합니다.")
                    break

            # 미리보기 (테스트용 - 필요 없으면 주석 처리)
            cv2.imshow("EyeCatch Bridge - Preview", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[종료] Ctrl+C 감지")

    # 정리
    pusher.stop()
    camera.close()
    cv2.destroyAllWindows()
    print(f"[종료] 총 {frame_count}프레임 전송 완료")


if __name__ == "__main__":
    main()
