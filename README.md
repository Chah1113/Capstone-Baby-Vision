# Capstone-Baby-VisionBabyGuard-AI
AI 기반 유아 안전 사고 예방 실시간 관제 시스템 > 2026학년도 1학기 기초캡스톤디자인

## 프로젝트 소개
본 프로젝트는 홈캠 영상을 실시간으로 분석하여 유아가 위험 구역(주방, 발코니 등)에 진입할 경우 보호자에게 즉각적인 알림을 보내는 지능형 사고 예방 시스템입니다.

## 주요 기능
실시간 영상 스트리밍: 홈캠(또는 웹캠) 영상을 앱으로 실시간 송출

AI 객체 인식: YOLO 모델을 통해 유아와 성인을 실시간으로 구분

위험 구역 설정: 사용자가 앱에서 직접 위험 구역(Virtual Fence) 지정

침범 감지 알고리즘: 유아가 설정 구역 진입 시 즉시 판별

푸시 알림: 위험 감지 시 스마트폰으로 즉각적인 소리 및 메시지 전림(FCM)

## 기술 스택
1. 언어 (Languages)
    Python: AI 모델 학습 및 영상 처리, 서버 개발에 사용 (메인 언어)

    Dart: Flutter를 이용한 안드로이드/iOS 앱 개발에 사용

2. 인공지능 및 영상 처리 (AI & Vision)
    YOLOv8 / v11: 영상 속에서 '사람'과 '유아'를 실시간으로 찾아내는 두뇌 역할

    OpenCV: 웹캠 영상을 읽어오고, 화면에 위험 구역 선을 그리는 시각 효과 담당

3. 백엔드 및 알림 (Backend & Notification)
    FastAPI: AI의 위험 감지 신호를 받아 앱으로 전달하는 가볍고 빠른 서버

    Firebase (FCM): 스마트폰으로 "위험!" 푸시 알림을 보내주는 구글 서비스

4. 모바일 앱 (Mobile App)
    Flutter: 안드로이드와 아이폰에서 동시에 작동하는 모니터링 앱 구현

## 프로젝트 구조

수정 가능성 多多

```
BabyGuard-AI/
├── .gitignore              # ⭐️ 중요! 깃허브에 올리지 말아야 할 파일 목록 (모델, 환경변수 등)
├── README.md               # 프로젝트 메인 설명서
│
├── ai/                     # [AI & Vision 파트]
│   ├── datasets/           # 학습용 데이터 (직접 찍은 사진 등 - .gitignore 필수)
│   ├── weights/            # 학습된 모델 파일 (best.pt 등)
│   ├── models/             # YOLOv8 추론용 소스 코드
│   ├── utils/              # OpenCV 구역 설정 및 전처리 함수
│   ├── main_vision.py      # 웹캠 실행 및 객체 인식 메인 스크립트
│   └── requirements.txt    # AI 실행을 위해 설치할 파이썬 라이브러리 목록
│
├── server/                 # [Backend 파트]
│   ├── app/                # FastAPI 소스 코드
│   │   ├── main.py         # 서버 실행 파일
│   │   ├── api/            # 알림(FCM), 구역 데이터 관련 API
│   │   └── core/           # 서버 설정 파일 (.env 등)
│   ├── requirements.txt    # 서버용 파이썬 라이브러리 목록
│   └── Dockerfile          # (선택) 서버 배포용 설정
│
├── app/                    # [Mobile App 파트 - Flutter]
│   ├── lib/                # 앱의 핵심 로직 (UI, 통신)
│   ├── assets/             # 앱에 들어갈 이미지, 아이콘
│   └── pubspec.yaml        # 앱 라이브러리 관리 파일
│
└── docs/                   # [문서 파트]
    ├── designs/            # 피그마 기획안, UI 설계도
    ├── reports/            # 주간 보고서, 최종 보고서 초안
    └── diagrams/           # 시스템 아키텍처 다이어그램 이미지
```

## 깃허브 규칙

1. 커밋 메시지는 정해진 규칙 따르기: 예) feat: 로그인 기능 추가, fix: 영상 끊김 버그 수정

2. 작업 전 Pull, 작업 후 Push: 항상 최신 코드를 유지

3 .Main 브랜치 직접 Push 금지: 각자 브랜치에서 작업 후 Pull Request를 통해 합치기

4. Merge는 하지마세요.
