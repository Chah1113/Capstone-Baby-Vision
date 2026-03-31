"""
영상 업로드 모듈
- 저장된 영상 파일을 메인 서버로 전송
- 서버 주소가 확정되면 config.py만 수정하면 됨
"""

import os
import requests
from config import MAIN_SERVER_URL


def upload_video(file_path: str) -> bool:
    """
    영상 파일을 메인 서버에 업로드한다.

    Args:
        file_path: 업로드할 영상 파일 경로

    Returns:
        성공 여부
    """
    if not os.path.exists(file_path):
        print(f"[오류] 파일이 존재하지 않습니다: {file_path}")
        return False

    upload_url = f"{MAIN_SERVER_URL}/api/upload/video"
    file_name = os.path.basename(file_path)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    print(f"[업로드] {file_name} ({file_size_mb:.1f}MB) → {upload_url}")

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_name, f, "video/mp4")}
            response = requests.post(upload_url, files=files, timeout=60)

        if response.status_code == 200:
            print(f"[업로드 완료] 서버 응답: {response.json()}")
            return True
        else:
            print(f"[업로드 실패] 상태 코드: {response.status_code}")
            print(f"[업로드 실패] 응답: {response.text}")
            return False

    except requests.ConnectionError:
        print(f"[업로드 실패] 서버에 연결할 수 없습니다: {upload_url}")
        print("[안내] config.py의 MAIN_SERVER_URL을 확인하세요.")
        return False
    except Exception as e:
        print(f"[업로드 실패] 예외 발생: {e}")
        return False


if __name__ == "__main__":
    # 단독 실행 테스트
    import sys
    if len(sys.argv) < 2:
        print("사용법: python uploader.py <영상파일경로>")
        print("예시: python uploader.py recordings/rec_20260331_140000.mp4")
    else:
        upload_video(sys.argv[1])
