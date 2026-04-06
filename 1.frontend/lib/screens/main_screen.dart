import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

// 1. 만들어둔 다른 화면 파일들을 불러옵니다.
import 'zone_screen.dart';
import 'settings_screen.dart';
import 'history_screen.dart'; // 사건 내역 화면 파일

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;
  String _userName = '';

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    final prefs = await SharedPreferences.getInstance();
    final userDataString = prefs.getString('eyeCatchUser');
    if (userDataString != null) {
      final userData = jsonDecode(userDataString);
      setState(() {
        _userName = userData['name'] ?? '보호자';
      });
    } else {
      if (!mounted) return;
      Navigator.pushReplacementNamed(context, '/login');
    }
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index; // 탭을 누르면 이 번호가 바뀝니다.
    });
  }

  void _handleLogout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('eyeCatchToken');
    await prefs.remove('eyeCatchUser');
    
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('안전하게 로그아웃 되었습니다.')),
    );
    Navigator.pushReplacementNamed(context, '/login');
  }

  // 2. 메인(모니터링) 화면을 별도의 위젯으로 분리했습니다.
  // (ZoneScreen과 SettingsScreen이 자체 AppBar를 갖고 있어서 화면이 겹치지 않게 분리)
  Widget _buildMonitoringScreen() {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Eye Catch', style: TextStyle(fontWeight: FontWeight.bold)),
        leading: const Icon(Icons.home, color: Colors.blue),
        actions: [
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8.0),
              child: Text('$_userName 보호자님', style: const TextStyle(fontSize: 14)),
            ),
          ),
          TextButton(
            onPressed: _handleLogout,
            child: const Text('로그아웃'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '실시간 아이방 상황',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            GestureDetector(
              onTap: () {
                // Navigator.pushNamed(context, '/live-stream');
              },
              child: Container(
                height: 200,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(16),
                  image: const DecorationImage(
                    image: NetworkImage('https://images.unsplash.com/photo-1596131398991-b94f928d85a1?auto=format&fit=crop&q=80'),
                    fit: BoxFit.cover,
                    opacity: 0.6,
                  ),
                ),
                child: const Center(
                  child: Icon(Icons.play_circle_fill, color: Colors.white, size: 64),
                ),
              ),
            ),
            const SizedBox(height: 16),
            Card(
              child: ListTile(
                leading: const Icon(Icons.warning, color: Colors.red),
                title: const Text('아이방 움직임 감지 (주의)'),
                subtitle: const Text('구역 1: 침대 주변 (방금 전)'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  // Navigator.pushNamed(context, '/incident-details');
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 3. 핵심 수정 포인트: IndexedStack을 사용해 화면 전환
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          _buildMonitoringScreen(), // 0번 탭: 모니터링 화면
          const ZoneScreen(),       // 1번 탭: 구역 설정 화면
          const HistoryScreen(),    // 2번 탭: 사건 내역 화면
          const SettingsScreen(),   // 3번 탭: 환경 설정 화면
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(icon: Icon(Icons.videocam), label: '모니터링'),
          BottomNavigationBarItem(icon: Icon(Icons.grid_view), label: '구역'),
          BottomNavigationBarItem(icon: Icon(Icons.warning), label: '사건 내역'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: '설정'),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.blue[800],
        unselectedItemColor: Colors.grey,
        onTap: _onItemTapped,
      ),
    );
  }
}