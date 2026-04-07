import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class AlertService {
  // 실제 서버 IP 또는 도메인으로 변경하세요. 
  static const String baseUrl = 'http://localhost:8000';

  // 헤더에 토큰을 주입하는 유틸리티 메서드
  static Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('eyeCatchToken') ?? '';
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token', // FastAPI의 decode_access_token과 매칭
    };
  }

  /// 1. 알림 목록 가져오기 (GET /alerts)
  static Future<List<dynamic>> fetchAlerts() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl/alerts'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        // UTF-8 디코딩 처리를 해주어야 한글이 깨지지 않습니다.
        return jsonDecode(utf8.decode(response.bodyBytes));
      } else {
        throw Exception('알림을 불러오는데 실패했습니다: ${response.statusCode}');
      }
    } catch (e) {
      print('fetchAlerts Error: $e');
      throw Exception('네트워크 오류가 발생했습니다.');
    }
  }

  /// 2. 특정 알림 읽음 처리하기 (PATCH /alerts/{alert_id}/read)
  static Future<void> markAlertAsRead(int alertId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.patch(
        Uri.parse('$baseUrl/alerts/$alertId/read'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        print('알림 읽음 처리 완료');
      } else {
        throw Exception('읽음 처리에 실패했습니다: ${response.statusCode}');
      }
    } catch (e) {
      print('markAlertAsRead Error: $e');
      throw Exception('네트워크 오류가 발생했습니다.');
    }
  }
}