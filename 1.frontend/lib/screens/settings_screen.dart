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
    final userDataString = prefs.getString('eyeCatchUser');
    if (userDataString != null) {
      final userData = jsonDecode(userDataString);
      setState(() {
        _profileName = userData['name'] ?? '보호자';
        _profileEmail = userData['email'] ?? 'parent@eyecatch.ai';
      });
    }
    setState(() => _isDarkMode = prefs.getString('theme') == 'dark');
  }

  Future<void> _handleLogout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('eyeCatchToken');
    await prefs.remove('eyeCatchUser');
    if (!mounted) return;
    ScaffoldMessenger.of(context)
        .showSnackBar(const SnackBar(content: Text('안전하게 로그아웃 되었습니다.')));
    Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
  }

  Future<void> _toggleDarkMode(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    setState(() => _isDarkMode = value);
    await prefs.setString('theme', value ? 'dark' : 'light');
    themeNotifier.value = value ? ThemeMode.dark : ThemeMode.light;
  }

  void _showPasswordCheckDialog() {
    final passwordController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('비밀번호 확인'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('개인정보를 수정하려면 비밀번호를 다시 입력해주세요.',
                style: TextStyle(fontSize: 14)),
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
            onPressed: () async {
              final password = passwordController.text;
              if (password.isEmpty) return;
              try {
                final response = await http.post(
                  Uri.parse('${AppConfig.baseUrl}/users/login'),
                  headers: {'Content-Type': 'application/json'},
                  body: jsonEncode({'email': _profileEmail, 'password': password}),
                );
                if (!context.mounted) return;
                if (response.statusCode == 200) {
                  Navigator.pop(context);
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const ProfileEditScreen()),
                  ).then((_) => _loadSettings());
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
            style: ElevatedButton.styleFrom(
              // 하드코딩 제거, 테마 primary 색상 사용
              backgroundColor: Theme.of(context).colorScheme.primary,
            ),
            child: Text('확인', style: TextStyle(color: Theme.of(context).colorScheme.onPrimary)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      backgroundColor: colorScheme.surface,
      appBar: AppBar(
        title: Row(
          children: [
            Icon(Icons.home, color: colorScheme.primary),
            const SizedBox(width: 8),
            Text('Eye Catch',
                style: TextStyle(color: colorScheme.primary, fontWeight: FontWeight.bold)),
          ],
        ),
        actions: [
          IconButton(
              icon: const Icon(Icons.notifications, color: Colors.grey), onPressed: () {}),
          const Padding(
            padding: EdgeInsets.only(right: 16.0),
            child: CircleAvatar(
              backgroundColor: Colors.grey,
              radius: 16,
              child: Icon(Icons.person, color: Colors.white, size: 20),
            ),
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
                color: Theme.of(context).cardColor, // 다크모드에 맞춰 자동 변환
                borderRadius: BorderRadius.circular(32),
                boxShadow: [
                  BoxShadow(
                    // 그림자 색상도 다크모드에서는 연하게 처리
                    color: Theme.of(context).shadowColor.withOpacity(0.05),
                    blurRadius: 10
                  )
                ],
              ),
              child: Column(
                children: [
                  const CircleAvatar(
                    radius: 50,
                    backgroundImage: NetworkImage(
                        'https://images.unsplash.com/photo-1596131398991-b94f928d85a1?auto=format&fit=crop&q=80'),
                  ),
                  const SizedBox(height: 16),
                  Text('$_profileName 보호자님',
                      style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  Text('맘앤대디 안심 계정', style: TextStyle(color: colorScheme.onSurfaceVariant)),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _buildBadge(context, '패밀리 리더', isPrimary: true),
                      const SizedBox(width: 8),
                      _buildBadge(context, '관리자 권한', isPrimary: false),
                    ],
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: _handleLogout,
                    icon: const Icon(Icons.logout),
                    label: const Text('로그아웃', style: TextStyle(fontWeight: FontWeight.bold)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: colorScheme.primary,
                      foregroundColor: colorScheme.onPrimary,
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
              context: context,
              title: '보호자 정보 수정',
              subtitle: _profileName,
              icon: Icons.person,
              onTap: _showPasswordCheckDialog,
            ),
            _buildListTile(
              context: context,
              title: '비상 연락처 (이메일)',
              subtitle: _profileEmail,
              icon: Icons.chevron_right,
            ),
            const SizedBox(height: 24),
            const Text('아이 안심 환경 설정',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildToggleTile(
              context: context,
              title: '아이 활동 알림',
              subtitle: '위험 구역 접근 및 울음소리 감지 시 즉시 알림',
              icon: Icons.notifications_active,
              value: _isAlertOn,
              onChanged: (val) => setState(() => _isAlertOn = val),
            ),
            _buildToggleTile(
              context: context,
              title: '야간 모드 (다크)',
              subtitle: '어두운 방에서 모니터링 시 눈 보호',
              icon: Icons.dark_mode,
              value: _isDarkMode,
              onChanged: _toggleDarkMode,
            ),
            _buildListTile(
              context: context,
              title: '앱 언어 설정',
              subtitle: '한국어 (Korean)',
              leadingIcon: Icons.language,
              icon: Icons.chevron_right,
            ),
            _buildListTile(
              context: context,
              title: '성장 기록 및 추억 저장소',
              subtitle: '감지된 활동 영상 90일 보관',
              leadingIcon: Icons.favorite,
              icon: Icons.chevron_right,
            ),
          ],
        ),
      ),
    );
  }

  // 색상을 테마 기반으로 변경
  Widget _buildBadge(BuildContext context, String text, {bool isPrimary = false}) {
    final colorScheme = Theme.of(context).colorScheme;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: isPrimary ? colorScheme.primaryContainer : colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(16)
      ),
      child: Text(text,
          style: TextStyle(
            color: isPrimary ? colorScheme.onPrimaryContainer : colorScheme.onSurfaceVariant,
            fontSize: 12,
            fontWeight: FontWeight.bold
          )),
    );
  }

  Widget _buildListTile({
    required BuildContext context,
    required String title,
    required String subtitle,
    required IconData icon,
    IconData? leadingIcon,
    VoidCallback? onTap,
  }) {
    final colorScheme = Theme.of(context).colorScheme;
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor, // 자동으로 테마에 맞춤
        borderRadius: BorderRadius.circular(16)
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              if (leadingIcon != null) ...[
                Icon(leadingIcon, color: colorScheme.onSurfaceVariant),
                const SizedBox(width: 16),
              ],
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    Text(subtitle, style: TextStyle(color: colorScheme.onSurfaceVariant, fontSize: 12)),
                  ],
                ),
              ),
              Icon(icon, color: colorScheme.onSurfaceVariant),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildToggleTile({
    required BuildContext context,
    required String title,
    required String subtitle,
    required IconData icon,
    required bool value,
    required ValueChanged<bool> onChanged,
  }) {
    final colorScheme = Theme.of(context).colorScheme;
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor, 
        borderRadius: BorderRadius.circular(16)
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: value ? colorScheme.primaryContainer : colorScheme.surfaceContainerHighest,
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: value ? colorScheme.primary : colorScheme.onSurfaceVariant),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                Text(subtitle, style: TextStyle(color: colorScheme.onSurfaceVariant, fontSize: 12)),
              ],
            ),
          ),
          Switch(value: value, onChanged: onChanged, activeColor: colorScheme.primary),
        ],
      ),
    );
  }
}

class ProfileEditScreen extends StatefulWidget {
  const ProfileEditScreen({super.key});

  @override
  State<ProfileEditScreen> createState() => _ProfileEditScreenState();
}

class _ProfileEditScreenState extends State<ProfileEditScreen> {
  // ... 기존과 동일하게 유지
  final _nameController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadCurrentInfo();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _loadCurrentInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final userDataString = prefs.getString('eyeCatchUser');
    if (userDataString != null) {
      final userData = jsonDecode(userDataString);
      setState(() => _nameController.text = userData['name'] ?? '보호자');
    }
  }

  Future<void> _saveInfo() async {
    // ... 기존 로직과 완전 동일
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('eyeCatchToken');
    if (token == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('로그인 정보가 없습니다.')));
      return;
    }

    final newName = _nameController.text.trim();
    final newPassword = _passwordController.text.trim();
    final Map<String, dynamic> updateData = {};
    if (newName.isNotEmpty) updateData['name'] = newName;
    if (newPassword.isNotEmpty) updateData['password'] = newPassword;

    if (updateData.isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('변경된 내용이 없습니다.')));
      return;
    }

    try {
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
        final userDataString = prefs.getString('eyeCatchUser');
        if (userDataString != null && newName.isNotEmpty) {
          final userData = jsonDecode(userDataString) as Map<String, dynamic>;
          userData['name'] = newName;
          await prefs.setString('eyeCatchUser', jsonEncode(userData));
        }
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('정보가 성공적으로 수정되었습니다.')),
        );
      } else {
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('정보 수정에 실패했습니다.')));
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('서버와의 통신에 실패했습니다.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    
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
              decoration: const InputDecoration(labelText: '이름 변경', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: '새 비밀번호', border: OutlineInputBorder()),
              obscureText: true,
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: _saveInfo,
              style: ElevatedButton.styleFrom(
                backgroundColor: colorScheme.primary, // 테마 색상 적용
                foregroundColor: colorScheme.onPrimary,
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