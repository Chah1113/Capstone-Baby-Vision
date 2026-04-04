"""
Firebase Cloud Messaging (FCM) 푸시 알림 모듈

TODO: 메인 서버 담당자가 구현
- Firebase Admin SDK 초기화
- 푸시 알림 전송 함수
"""

# import firebase_admin
# from firebase_admin import credentials, messaging

# Firebase 초기화 (서버 시작 시 1회 실행)
# cred = credentials.Certificate("path/to/firebase-key.json")
# firebase_admin.initialize_app(cred)


async def send_push_notification(fcm_token: str, title: str, body: str):
    """
    특정 디바이스에 푸시 알림을 보낸다.

    Args:
        fcm_token: 대상 디바이스의 FCM 토큰
        title: 알림 제목 (예: "⚠️ 위험 감지!")
        body: 알림 내용 (예: "유아가 주방 구역에 진입했습니다.")
    """
    # TODO: Firebase Admin SDK로 실제 전송 구현
    # message = messaging.Message(
    #     notification=messaging.Notification(title=title, body=body),
    #     token=fcm_token,
    # )
    # response = messaging.send(message)
    print(f"[FCM] 알림 전송 (미구현): {title} - {body}")


async def send_topic_notification(topic: str, title: str, body: str):
    """
    특정 토픽을 구독한 모든 디바이스에 알림을 보낸다.

    Args:
        topic: FCM 토픽 이름 (예: "baby_alerts")
        title: 알림 제목
        body: 알림 내용
    """
    # TODO: 토픽 기반 알림 전송 구현
    print(f"[FCM] 토픽 알림 전송 (미구현): [{topic}] {title} - {body}")
