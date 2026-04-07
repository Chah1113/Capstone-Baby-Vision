import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'zone_screen.dart';
import 'settings_screen.dart';
import 'history_screen.dart';
import 'live_stream_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

// 애니메이션을 위해 SingleTickerProviderStateMixin 추가
class _MainScreenState extends State<MainScreen> with SingleTickerProviderStateMixin {
  int _selectedIndex = 0;
  String _userName = '';
  
  late AnimationController _alertAnimController;

  @override
  void initState() {
    super.initState();
    _loadUserData();
    
    // 알림 카드 애니메이션 컨트롤러 (0.4초 동안 팝 효과)
    _alertAnimController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400),
    );
  }

  @override
  void dispose() {
    _alertAnimController.dispose();
    super.dispose();
  }

  Future<void> _loadUserData() async {
    final prefs = await SharedPreferences.getInstance();
    final userDataString = prefs.getString('eyeCatchUser');
    if (userDataString != null) {
      final userData = jsonDecode(userDataString);
      setState(() => _userName = userData['name'] ?? '보호자');
    } else {
      if (!mounted) return;
      Navigator.pushReplacementNamed(context, '/login');
    }
  }

  void _onItemTapped(int index) => setState(() => _selectedIndex = index);

  Future<void> _handleLogout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('eyeCatchToken');
    await prefs.remove('eyeCatchUser');
    if (!mounted) return;
    ScaffoldMessenger.of(context)
        .showSnackBar(const SnackBar(content: Text('안전하게 로그아웃 되었습니다.')));
    Navigator.pushReplacementNamed(context, '/login');
  }

  Widget _buildMonitoringScreen() {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Eye Catch', style: TextStyle(fontWeight: FontWeight.bold)),
        leading: Icon(Icons.home, color: Theme.of(context).colorScheme.primary),
        actions: [
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8.0),
              child: Text('$_userName 보호자님', style: const TextStyle(fontSize: 14)),
            ),
          ),
          TextButton(onPressed: _handleLogout, child: const Text('로그아웃')),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          // 1. 애니메이션 트리거 (진동/색상 효과 재생 후 되감기)
          _alertAnimController.forward().then((_) => _alertAnimController.reverse());
          
          // 2. 스낵바 알람
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('🚨 위험 구역 접근이 감지되었습니다!'),
              backgroundColor: Colors.redAccent,
              behavior: SnackBarBehavior.floating,
            ),
          );
        },
        backgroundColor: Colors.redAccent,
        icon: const Icon(Icons.add_alert, color: Colors.white),
        label: const Text('알람 테스트',
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('실시간 아이방 상황',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            GestureDetector(
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const LiveStreamScreen()),
              ),
              child: Container(
                height: 200,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(16),
                  image: const DecorationImage(
                    image: NetworkImage(
                        'https://images.unsplash.com/photo-1596131398991-b94f928d85a1?auto=format&fit=crop&q=80'),
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
            
            // 애니메이션이 적용된 로그 카드
            AnimatedBuilder(
              animation: _alertAnimController,
              builder: (context, child) {
                // 확대 스케일 (기본 1.0 -> 최대 1.05배 확대)
                final scale = 1.0 + (_alertAnimController.value * 0.05);
                // 붉은색 그라데이션 배경 전환
                final bgColor = Color.lerp(
                  Theme.of(context).cardColor, 
                  Colors.redAccent.withOpacity(0.3), 
                  _alertAnimController.value
                );

                return Transform.scale(
                  scale: scale,
                  child: Card(
                    color: bgColor,
                    elevation: _alertAnimController.value > 0 ? 8 : 1, // 떠오르는 그림자 효과
                    child: ListTile(
                      leading: const Icon(Icons.warning, color: Colors.red),
                      title: const Text('아이방 움직임 감지 (주의)', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: const Text('구역 1: 침대 주변 (방금 전)'),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () {},
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          _buildMonitoringScreen(),
          const ZoneScreen(),
          const HistoryScreen(),
          const SettingsScreen(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.videocam), label: '모니터링'),
          BottomNavigationBarItem(icon: Icon(Icons.grid_view), label: '구역'),
          BottomNavigationBarItem(icon: Icon(Icons.warning), label: '사건 내역'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: '설정'),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Theme.of(context).colorScheme.primary,
        unselectedItemColor: Theme.of(context).colorScheme.onSurfaceVariant,
        onTap: _onItemTapped,
      ),
    );
  }
}