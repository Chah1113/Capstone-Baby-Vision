import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../main.dart'; 

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  String _profileName = '보호자';
  String _profileEmail = 'parent@eyecatch.ai';
  bool _isAlertOn = true;
  bool _isDarkMode = false;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    // 유저 정보 불러오기
    final userDataString = prefs.getString('eyeCatchUser');
    if (userDataString != null) {
      final userData = jsonDecode(userDataString);
      setState(() {
        _profileName = userData['name'] ?? '보호자';
        _profileEmail = userData['email'] ?? 'parent@eyecatch.ai';
      });
    }

    // 테마 설정 불러오기
    setState(() {
      _isDarkMode = prefs.getString('theme') == 'dark';
    });
  }
  
  void _handleLogout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('eyeCatchToken');
    await prefs.remove('eyeCatchUser');
    
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('안전하게 로그아웃 되었습니다.')));
    Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
  }

  Future<void> _toggleDarkMode(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _isDarkMode = value;
    });
    await prefs.setString('theme', value ? 'dark' : 'light');
    themeNotifier.value = value ? ThemeMode.dark : ThemeMode.light;
  }

  void _showPasswordCheckDialog() {
    final TextEditingController passwordController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('비밀번호 확인'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('개인정보를 수정하려면 비밀번호를 다시 입력해주세요.', style: TextStyle(fontSize: 14)),
              const SizedBox(height: 16),
              TextField(
                controller: passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: '현재 비밀번호',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('취소', style: TextStyle(color: Colors.grey)),
            ),
            ElevatedButton(
              // async 추가
              onPressed: () async {
                final password = passwordController.text;
                if (password.isEmpty) return;

                try {
                  // 기존 로그인 API를 활용하여 비밀번호가 맞는지 서버에 검증
                  final response = await http.post(
                    Uri.parse('${AppConfig.baseUrl}/users/login'),
                    headers: {'Content-Type': 'application/json'},
                    body: jsonEncode({
                      'email': _profileEmail,
                      'password': password
                    }),
                  );

                  if (!context.mounted) return;

                  if (response.statusCode == 200) {
                    Navigator.pop(context); // 다이얼로그 닫기
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const ProfileEditScreen()),
                    ).then((_) {
                      _loadSettings(); 
                    });
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('비밀번호가 일치하지 않습니다.')),
                    );
                  }
                } catch (e) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('서버와 연결할 수 없습니다.')),
                  );
                }
              },
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF003d9b)),
              child: const Text('확인', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      appBar: AppBar(
        title: const Row(
          children: [
            Icon(Icons.home, color: Color(0xFF003d9b)),
            SizedBox(width: 8),
            Text('Eye Catch', style: TextStyle(color: Color(0xFF003d9b), fontWeight: FontWeight.bold)),
          ],
        ),
        actions: [
          IconButton(icon: const Icon(Icons.notifications, color: Colors.grey), onPressed: () {}),
          const Padding(
            padding: EdgeInsets.only(right: 16.0),
            child: CircleAvatar(backgroundColor: Colors.grey, radius: 16, child: Icon(Icons.person, color: Colors.white, size: 20)),
          ),
        ],
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(32),
                boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10)],
              ),
              child: Column(
                children: [
                  const CircleAvatar(
                    radius: 50,
                    backgroundImage: NetworkImage('https://images.unsplash.com/photo-1596131398991-b94f928d85a1?auto=format&fit=crop&q=80'),
                  ),
                  const SizedBox(height: 16),
                  Text('$_profileName 보호자님', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  const Text('맘앤대디 안심 계정', style: TextStyle(color: Colors.grey)),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(color: Colors.blue[50], borderRadius: BorderRadius.circular(16)),
                        child: Text('패밀리 리더', style: TextStyle(color: Colors.blue[800], fontSize: 12, fontWeight: FontWeight.bold)),
                      ),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(16)),
                        child: const Text('관리자 권한', style: TextStyle(color: Colors.black54, fontSize: 12, fontWeight: FontWeight.bold)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: _handleLogout,
                    icon: const Icon(Icons.logout),
                    label: const Text('로그아웃', style: TextStyle(fontWeight: FontWeight.bold)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF003d9b),
                      foregroundColor: Colors.white,
                      minimumSize: const Size(double.infinity, 48),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            const Text('계정 관리', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildListTile(
              title: '보호자 정보 수정', 
              subtitle: _profileName, 
              icon: Icons.person,
              onTap: _showPasswordCheckDialog,
            ),
            _buildListTile(title: '비상 연락처 (이메일)', subtitle: _profileEmail, icon: Icons.chevron_right),
            
            const SizedBox(height: 24),
            
            const Text('아이 안심 환경 설정', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildToggleTile(
              title: '아이 활동 알림',
              subtitle: '위험 구역 접근 및 울음소리 감지 시 즉시 알림',
              icon: Icons.notifications_active,
              value: _isAlertOn,
              onChanged: (val) => setState(() => _isAlertOn = val),
            ),
            _buildToggleTile(
              title: '야간 모드 (다크)',
              subtitle: '어두운 방에서 모니터링 시 눈 보호',
              icon: Icons.dark_mode,
              value: _isDarkMode,
              onChanged: _toggleDarkMode,
            ),
            _buildListTile(title: '앱 언어 설정', subtitle: '한국어 (Korean)', leadingIcon: Icons.language, icon: Icons.chevron_right),
            _buildListTile(title: '성장 기록 및 추억 저장소', subtitle: '감지된 활동 영상 90일 보관', leadingIcon: Icons.favorite, icon: Icons.chevron_right),
          ],
        ),
      ),
    );
  }

  Widget _buildListTile({required String title, required String subtitle, required IconData icon, IconData? leadingIcon, VoidCallback? onTap}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              if (leadingIcon != null) ...[
                Icon(leadingIcon, color: Colors.grey),
                const SizedBox(width: 16),
              ],
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)),
                  ],
                ),
              ),
              Icon(icon, color: Colors.grey),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildToggleTile({
    required String title,
    required String subtitle,
    required IconData icon,
    required bool value,
    required ValueChanged<bool> onChanged,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(color: value ? Colors.blue[50] : Colors.grey[100], shape: BoxShape.circle),
            child: Icon(icon, color: value ? Colors.blue[700] : Colors.grey),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)),
              ],
            ),
          ),
          Switch(
            value: value,
            onChanged: onChanged,
            activeColor: Colors.blue[700],
          ),
        ],
      ),
    );
  }
}

// 🔥 수정됨: StatelessWidget에서 StatefulWidget으로 변경하여 데이터 저장 및 UI 갱신 로직 추가
class ProfileEditScreen extends StatefulWidget {
  const ProfileEditScreen({super.key});

  @override
  State<ProfileEditScreen> createState() => _ProfileEditScreenState();
}

class _ProfileEditScreenState extends State<ProfileEditScreen> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadCurrentInfo();
  }

  Future<void> _loadCurrentInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final userDataString = prefs.getString('eyeCatchUser');
    if (userDataString != null) {
      final userData = jsonDecode(userDataString);
      setState(() {
        _nameController.text = userData['name'] ?? '보호자';
      });
    }
  }

  Future<void> _saveInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('eyeCatchToken'); // 저장된 토큰 가져오기

    if (token == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('로그인 정보가 없습니다.')));
      return;
    }

    final newName = _nameController.text.trim();
    final newPassword = _passwordController.text.trim();

    // 보낼 데이터 구성 (빈 값이 아니면 변경사항에 포함)
    Map<String, dynamic> updateData = {};
    if (newName.isNotEmpty) updateData['name'] = newName;
    if (newPassword.isNotEmpty) updateData['password'] = newPassword;

    if (updateData.isEmpty) {
       ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('변경된 내용이 없습니다.')));
       return;
    }

    try {
      // 위에서 생성한 백엔드 API (PUT /users/me) 호출
      final response = await http.put(
        Uri.parse('${AppConfig.baseUrl}/users/me'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: jsonEncode(updateData),
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        // 서버 업데이트 성공 시, 내부 저장소의 유저 이름도 업데이트
        final userDataString = prefs.getString('eyeCatchUser');
        if (userDataString != null) {
          Map<String, dynamic> userData = jsonDecode(userDataString);
          if (newName.isNotEmpty) {
            userData['name'] = newName;
            await prefs.setString('eyeCatchUser', jsonEncode(userData));
          }
        }
        
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('정보가 성공적으로 수정되었습니다.')),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('정보 수정에 실패했습니다.')),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('서버와의 통신에 실패했습니다.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('보호자 정보 수정', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: '이름 변경',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(
                labelText: '새 비밀번호',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: _saveInfo,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF003d9b),
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 50),
              ),
              child: const Text('저장하기', style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}