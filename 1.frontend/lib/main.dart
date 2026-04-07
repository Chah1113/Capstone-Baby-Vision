import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
//import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:google_fonts/google_fonts.dart';

import 'screens/login_screen.dart';
import 'screens/main_screen.dart';
import 'screens/live_stream_screen.dart'; // 라우팅 추가
//import 'services/notification_service.dart';

final ValueNotifier<ThemeMode> themeNotifier = ValueNotifier(ThemeMode.system);

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // ==========================================
  // 🚨 창이 안 뜨는 원인: Firebase 및 알림 초기화
  // 현재 완벽한 Firebase 세팅이 되어있지 않거나 Windows로 실행 중이면 여기서 멈춥니다.
  // UI 수정을 먼저 확인하기 위해 잠시 주석(//) 처리합니다.
  // ==========================================
  
  try {
    // await Firebase.initializeApp();
    // final notificationService = NotificationService();
    // await notificationService.initialize();
    // await notificationService.requestPermission();
  } catch (e) {
    debugPrint('알림 초기화 에러 (무시 가능): $e');
  }

  // ==========================================

  final prefs = await SharedPreferences.getInstance();
  final themeStr = prefs.getString('theme');
  if (themeStr == 'dark') {
    themeNotifier.value = ThemeMode.dark;
  } else if (themeStr == 'light') {
    themeNotifier.value = ThemeMode.light;
  }

  runApp(const EyeCatchApp());
}

class EyeCatchApp extends StatelessWidget {
  const EyeCatchApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeNotifier,
      builder: (_, ThemeMode currentMode, __) {
        return MaterialApp(
          // 3. NotificationService의 navigatorKey를 연결
          //navigatorKey: NotificationService.navigatorKey, 
          title: 'Eye Catch',
          localizationsDelegates: const [
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('ko', 'KR'),
            Locale('en', 'US'),
          ],
          locale: const Locale('ko', 'KR'),
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF003d9b), brightness: Brightness.light),
            useMaterial3: true,
            textTheme: GoogleFonts.notoSansKrTextTheme(ThemeData.light().textTheme),
          ),
          darkTheme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF60a5fa), brightness: Brightness.dark),
            useMaterial3: true,
            textTheme: GoogleFonts.notoSansKrTextTheme(ThemeData.dark().textTheme),
          ),
          themeMode: currentMode,
          initialRoute: '/login',
          routes: {
            '/login': (context) => const LoginScreen(),
            '/main': (context) => const MainScreen(),
            '/live-stream': (context) => const LiveStreamScreen(), // 액션 라우팅용 추가
          },
        );
      },
    );
  }
}