import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config.dart'; 

class AlertService {
  static String get baseUrl => AppConfig.baseUrl;

  static Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('eyeCatchToken') ?? '';
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  static Future<List<dynamic>> fetchAlerts() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl/alerts'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return jsonDecode(utf8.decode(response.bodyBytes));
      } else {
        throw Exception('알림을 불러오는데 실패했습니다: ${response.statusCode}');
      }
    } catch (e) {
      print('fetchAlerts Error: $e');
      throw Exception('네트워크 오류가 발생했습니다.');
    }
  }

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

  /// [추가됨] 임시 테스트용 알림 발생 메서드
  static Future<void> triggerTestAlert() async {
    try {
      final headers = await _getHeaders();
      // 백엔드에 테스트 알림을 생성하는 엔드포인트가 있다고 가정한 요청입니다.
      final response = await http.post(
        Uri.parse('$baseUrl/alerts/test'), 
        headers: headers,
        body: jsonEncode({
          'message': '테스트 위험 감지 알림입니다.',
          'zone': '침대 주변',
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('테스트 알림 전송 완료');
      } else {
        print('테스트 알림 전송 실패: ${response.statusCode}');
      }
    } catch (e) {
      print('triggerTestAlert Error: $e');
    }
  }
}