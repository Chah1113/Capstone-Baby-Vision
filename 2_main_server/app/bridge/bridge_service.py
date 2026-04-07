"""
Bridge Service - 카메라 영상을 MediaMTX로 전송
"""
import threading
import time
from .camera import CameraReader
from .rtsp_pusher import RtspPusher


class BridgeService:
    """
    카메라에서 읽은 영상을 MediaMTX로 push하는 서비스
    """
    
    def __init__(self, camera_source, rtsp_url: str, width: int, height: int, fps: int):
        self.camera = CameraReader(camera_source, width, height)
        self.pusher = RtspPusher(rtsp_url, width, height, fps)
        self.running = False
        self.thread = None
        self.fps = fps
    
    def start(self) -> bool:
        """Bridge 서비스 시작"""
        print("\n========================================")
        print("  Bridge Service Starting...")
        print("========================================")
        
        # 1. 카메라 연결
        print("[1/3] 카메라 연결 중...")
        if not self.camera.open():
            print("[오류] 카메라 연결 실패")
            return False
        
        # 2. RTSP Pusher 시작
        print("[2/3] RTSP Pusher 시작 중...")
        if not self.pusher.start():
            print("[오류] RTSP Pusher 시작 실패")
            self.camera.close()
            return False
        
        # 3. 백그라운드 스레드 시작
        print("[3/3] 영상 전송 시작...")
        self.running = True
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()
        
        print("========================================")
        print("  ✅ Bridge Service Ready!")
        print(f"  - Camera: {self.camera.source}")
        print(f"  - RTSP: {self.pusher.rtsp_url}")
        print("========================================\n")
        
        return True
    
    def _stream_loop(self):
        """영상 전송 루프 (백그라운드)"""
        interval = 1.0 / self.fps
        frame_count = 0
        fail_count = 0
        
        while self.running:
            frame = self.camera.read_frame()
            
            # 프레임 읽기 실패
            if frame is None:
                fail_count += 1
                if fail_count >= 30:
                    print("[Bridge] 프레임 읽기 실패. 재연결 시도...")
                    if not self.camera.reconnect():
                        print("[Bridge] 재연결 실패. 서비스 중단.")
                        self.running = False
                        break
                    fail_count = 0
                time.sleep(0.1)
                continue
            
            fail_count = 0
            frame_count += 1
            
            # MediaMTX로 전송
            if not self.pusher.push_frame(frame):
                print("[Bridge] RTSP 전송 실패. 재시작 시도...")
                self.pusher.stop()
                time.sleep(1)
                if not self.pusher.start():
                    print("[Bridge] RTSP 재시작 실패. 서비스 중단.")
                    self.running = False
                    break
            
            # FPS 조절
            time.sleep(interval)
            
            # 로그 (10초마다)
            if frame_count % (self.fps * 10) == 0:
                print(f"[Bridge] 전송 중... ({frame_count} 프레임)")
        
        print(f"[Bridge] 서비스 종료 (총 {frame_count} 프레임 전송)")
    
    def stop(self):
        """Bridge 서비스 종료"""
        print("[Bridge] 종료 중...")
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=5)
        
        self.pusher.stop()
        self.camera.close()
        
        print("[Bridge] 종료 완료")
    
    def is_running(self) -> bool:
        """실행 상태 확인"""
        return self.running and self.camera.is_opened()
