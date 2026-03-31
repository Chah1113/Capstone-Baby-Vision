"""
EyeCatch 브릿지 서비스 메인 스크립트
- 카메라 영상 녹화 → 파일 저장 → 서버 업로드
- 한 번에 실행: python main.py
"""

from recorder import record_video
from uploader import upload_video


def main():
    print("=" * 50)
    print("  EyeCatch Bridge Service")
    print("=" * 50)

    # 1단계: 영상 녹화
    print("\n[1/2] 영상 녹화 시작...")
    saved_path = record_video(duration_sec=0)  # q키로 수동 종료

    if not saved_path:
        print("[중단] 녹화 실패. 종료합니다.")
        return

    # 2단계: 서버 업로드
    print(f"\n[2/2] 서버 업로드 시작...")
    success = upload_video(saved_path)

    if success:
        print("\n[완료] 녹화 + 업로드 성공!")
    else:
        print(f"\n[부분 완료] 영상은 저장됨: {saved_path}")
        print("[안내] 서버 주소 확정 후 다시 업로드 가능:")
        print(f"  python uploader.py {saved_path}")


if __name__ == "__main__":
    main()
