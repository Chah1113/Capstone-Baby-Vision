import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  // 입력값을 가져오기 위한 컨트롤러
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  
  bool _isLoading = false;

  // ⚠️ 백엔드 서버 주소
  final String apiUrl = 'http://localhost:8000'; 

  Future<void> _handleSignup() async {
    // 빈 칸 검사
    if (_nameController.text.isEmpty || 
        _emailController.text.isEmpty || 
        _passwordController.text.isEmpty) {
      _showSnackBar('모든 항목을 입력해주세요.');
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // 백엔드 (FastAPI)의 POST /users/register 엔드포인트 호출
      final response = await http.post(
        Uri.parse('$apiUrl/users/register'),
        headers: {
          'Content-Type': 'application/json',
          'ngrok-skip-browser-warning': '69420', // ngrok 사용 시 필요한 헤더
        },
        // 서버의 UserCreate 스키마에 맞춰 JSON 데이터 변환
        body: jsonEncode({
          'name': _nameController.text,
          'email': _emailController.text,
          'password': _passwordController.text,
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        if (!mounted) return;
        _showSnackBar('회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.');
        // 가입 성공 시 로그인 화면으로 돌아가기
        Navigator.pop(context); 
      } else {
        // 서버에서 보낸 에러 메시지 처리 (예: "이미 존재하는 이메일이에요")
        final errorData = jsonDecode(response.body);
        _showSnackBar('가입 실패: ${errorData['detail'] ?? '입력하신 정보를 확인해주세요.'}');
      }
    } catch (error) {
      _showSnackBar('서버와 통신할 수 없습니다. 서버가 켜져 있는지 확인해주세요.');
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _showSnackBar(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA), // 제공해주신 HTML의 배경색 적용
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios, color: Colors.grey),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          '로그인으로 돌아가기',
          style: TextStyle(color: Colors.grey, fontSize: 14),
        ),
        actions: const [
          Padding(
            padding: EdgeInsets.only(right: 16.0),
            child: Center(
              child: Text(
                'Eye Catch',
                style: TextStyle(color: Color(0xFF003d9b), fontWeight: FontWeight.bold, fontSize: 18),
              ),
            ),
          )
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '새로운 계정 만들기',
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, fontFamily: 'Manrope'),
              ),
              const SizedBox(height: 8),
              const Text(
                '안전관리 총괄 책임자 계정을 등록합니다.',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 40),
              
              // 입력 폼 영역 (HTML의 카드 스타일 적용)
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(24), // 둥근 모서리
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.04), 
                      blurRadius: 20, 
                      offset: const Offset(0, 4)
                    )
                  ],
                ),
                child: Column(
                  children: [
                    TextField(
                      controller: _nameController,
                      decoration: InputDecoration(
                        labelText: '이름',
                        prefixIcon: const Icon(Icons.person_outline, color: Color(0xFF737685)),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: const BorderSide(color: Color(0xFF003d9b), width: 2),
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _emailController,
                      decoration: InputDecoration(
                        labelText: '이메일 주소',
                        prefixIcon: const Icon(Icons.mail_outline, color: Color(0xFF737685)),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: const BorderSide(color: Color(0xFF003d9b), width: 2),
                        ),
                      ),
                      keyboardType: TextInputType.emailAddress,
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _passwordController,
                      decoration: InputDecoration(
                        labelText: '비밀번호',
                        prefixIcon: const Icon(Icons.lock_outline, color: Color(0xFF737685)),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: const BorderSide(color: Color(0xFF003d9b), width: 2),
                        ),
                      ),
                      obscureText: true,
                    ),
                    const SizedBox(height: 32),
                    
                    // 가입 버튼 (그라데이션 효과 대신 단색 브랜드 컬러 적용)
                    SizedBox(
                      width: double.infinity,
                      height: 54,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _handleSignup,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF003d9b),
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          elevation: 2,
                        ),
                        child: _isLoading
                            ? const SizedBox(
                                height: 24, 
                                width: 24, 
                                child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)
                              )
                            : const Text('회원가입 완료', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}