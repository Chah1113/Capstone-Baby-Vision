"""
카메라 연결 및 프레임 읽기
4_bridge_service/camera.py를 Main Server용으로 수정
"""
import cv2
import time


class CameraReader:
    """
    OpenCV로 카메라 영상을 읽는 클래스
    """
    
    def __init__(self, source=0, width=640, height=480):
        """
        Args:
            source: 카메라 소스 (0, 1, "rtsp://...", "/dev/video0" 등)
            width: 영상 너비
            height: 영상 높이
        """
        self.source = source
        self.width = width
        self.height = height
        self.cap = None
        
    def open(self) -> bool:
        """카메라 연결"""
        try:
            self.cap = cv2.VideoCapture(self.source)
            
            if not self.cap.isOpened():
                print(f"[Camera] 카메라 연결 실패: {self.source}")
                return False
            
            # 해상도 설정
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            
            # 테스트 프레임 읽기
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print(f"[Camera] 프레임 읽기 실패")
                return False
            
            # 실제 해상도 출력
            actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"[Camera] 카메라 연결 성공: {self.source} ({actual_w}x{actual_h})")
            
            return True
            
        except Exception as e:
            print(f"[Camera] 오류: {e}")
            return False
    
    def read_frame(self):
        """프레임 읽기"""
        if self.cap is None or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        
        if not ret or frame is None:
            return None
        
        # 해상도 맞추기 (필요시)
        if frame.shape[1] != self.width or frame.shape[0] != self.height:
            frame = cv2.resize(frame, (self.width, self.height))
        
        return frame
    
    def reconnect(self) -> bool:
        """카메라 재연결"""
        print("[Camera] 재연결 시도...")
        self.close()
        time.sleep(1)
        return self.open()
    
    def close(self):
        """카메라 연결 종료"""
        if self.cap:
            self.cap.release()
            self.cap = None
        print("[Camera] 카메라 연결 종료")
    
    def is_opened(self) -> bool:
        """카메라 연결 상태"""
        return self.cap is not None and self.cap.isOpened()
