FROM python:3.11

# 시스템 패키지 및 FFmpeg 설치
RUN apt-get update && apt-get install -y \
    wget \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# MediaMTX 다운로드 및 설치
RUN wget https://github.com/bluenviron/mediamtx/releases/download/v1.5.0/mediamtx_v1.5.0_linux_amd64.tar.gz && \
    tar -xzf mediamtx_v1.5.0_linux_amd64.tar.gz && \
    mv mediamtx /usr/local/bin/mediamtx && \
    rm mediamtx_v1.5.0_linux_amd64.tar.gz

# Python 의존성 설치
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 시작 스크립트 복사 및 실행 권한
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 포트 노출
EXPOSE 8000 8554

# 시작 스크립트 실행
CMD ["/start.sh"]
