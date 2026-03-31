"""
영상 녹화 모듈
- 카메라(또는 영상 소스)에서 프레임을 읽어서 파일로 저장
- 저장된 파일 경로를 반환
"""

import cv2
import os
import time
from datetime import datetime
from config import CAMERA_SOURCE, SAVE_DIR, SAVE_FPS, SAVE_RESOLUTION


def get_save_path() -> str:
    """타임스탬프 기반 저장 파일 경로를 생성한다."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(SAVE_DIR, f"rec_{timestamp}.mp4")


def record_video(duration_sec: int = 0) -> str:
    """
    카메라에서 영상을 받아 파일로 저장한다.

    Args:
        duration_sec: 녹화 시간(초). 0이면 q키로 수동 종료.

    Returns:
        저장된 파일 경로
    """
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    if not cap.isOpened():
        print(f"[오류] 카메라를 열 수 없습니다: {CAMERA_SOURCE}")
        return ""

    save_path = get_save_path()
    width, height = SAVE_RESOLUTION

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(save_path, fourcc, SAVE_FPS, (width, height))

    print(f"[녹화 시작] 저장 경로: {save_path}")
    if duration_sec > 0:
        print(f"[녹화] {duration_sec}초 후 자동 종료")
    else:
        print("[녹화] q 키를 누르면 종료")

    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[경고] 프레임을 읽을 수 없습니다. 종료합니다.")
            break

        # 해상도 맞추기
        frame = cv2.resize(frame, (width, height))
        writer.write(frame)
        frame_count += 1

        # 미리보기 (선택)
        cv2.imshow("EyeCatch Recording", frame)

        # 종료 조건
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("[녹화] 수동 종료")
            break
        if duration_sec > 0 and (time.time() - start_time) >= duration_sec:
            print("[녹화] 시간 도달, 자동 종료")
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    elapsed = time.time() - start_time
    print(f"[녹화 완료] {frame_count}프레임 / {elapsed:.1f}초 → {save_path}")
    return save_path


if __name__ == "__main__":
    # 단독 실행 테스트: 10초 녹화
    path = record_video(duration_sec=10)
    if path:
        print(f"저장 완료: {path}")
