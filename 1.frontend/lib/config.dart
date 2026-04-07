// lib/config.dart
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

class AppConfig {
  // baseUrl을 호출하면 앱이 실행 중인 환경을 파악해서 알맞은 주소를 반환합니다.
  static String get baseUrl {
    
    // 💡 나중에 앱을 실제 스토어에 출시할 때는 아래 주석을 풀고 실제 도메인을 넣으시면 됩니다.
    // return 'https://api.eyecatch.ai'; 

    // 웹 브라우저에서 실행 중인 경우
    if (kIsWeb) {
      return 'http://localhost:8000';
    } 
    // 안드로이드 기기(또는 에뮬레이터)에서 실행 중인 경우
    else if (Platform.isAndroid) {
      // 10.0.2.2는 안드로이드 에뮬레이터에서 내 컴퓨터를 가리키는 특수 주소입니다.
      // (만약 실제 안드로이드 스마트폰을 선으로 연결했다면 이 부분을 192.168.x.x 공유기 IP로 바꿔야 합니다)
      return 'http://10.0.2.2:8000';
    } 
    // iOS 시뮬레이터에서 실행 중인 경우
    else {
      return 'http://localhost:8000';
    }
  }
}