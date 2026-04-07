"""
MediaMTX로 RTSP push
4_bridge_service/rtsp_pusher.py를 Main Server용으로 수정
"""
import subprocess
import numpy as np


class RtspPusher:
    """
    FFmpeg를 사용하여 MediaMTX로 RTSP push
    """
    
    def __init__(self, rtsp_url: str, width: int = 640, height: int = 480, fps: int = 15):
        """
        Args:
            rtsp_url: MediaMTX RTSP 주소 (예: rtsp://localhost:8554/stream)
            width: 영상 너비
            height: 영상 높이
            fps: 초당 프레임 수
        """
        self.rtsp_url = rtsp_url
        self.width = width
        self.height = height
        self.fps = fps
        self.process = None
    
    def start(self) -> bool:
        """FFmpeg 프로세스 시작"""
        try:
            command = [
                'ffmpeg',
                '-y',  # 덮어쓰기
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-pix_fmt', 'bgr24',
                '-s', f'{self.width}x{self.height}',
                '-r', str(self.fps),
                '-i', 'pipe:0',  # stdin으로 프레임 받기
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-tune', 'zerolatency',
                '-f', 'rtsp',
                self.rtsp_url
            ]
            
            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            print(f"[RTSP] FFmpeg 시작: {self.rtsp_url}")
            return True
            
        except FileNotFoundError:
            print("[RTSP] FFmpeg가 설치되지 않았습니다!")
            return False
        except Exception as e:
            print(f"[RTSP] 시작 실패: {e}")
            return False
    
    def push_frame(self, frame: np.ndarray) -> bool:
        """프레임을 MediaMTX로 전송"""
        if self.process is None or self.process.poll() is not None:
            return False
        
        try:
            self.process.stdin.write(frame.tobytes())
            return True
        except BrokenPipeError:
            print("[RTSP] 연결 끊김")
            return False
        except Exception as e:
            print(f"[RTSP] 전송 실패: {e}")
            return False
    
    def stop(self):
        """FFmpeg 프로세스 종료"""
        if self.process:
            try:
                self.process.stdin.close()
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            
            self.process = None
            print("[RTSP] FFmpeg 종료")
