import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:google_fonts/google_fonts.dart';

import 'screens/login_screen.dart';
import 'screens/main_screen.dart';
import 'screens/onboarding_screen.dart'; // 방금 만든 온보딩 화면 임포트

final ValueNotifier<ThemeMode> themeNotifier = ValueNotifier(ThemeMode.system);

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 주석 처리 유지 (Firebase 세팅 전)
  // await Firebase.initializeApp();
  // final notificationService = NotificationService();
  // await notificationService.initialize();

  final prefs = await SharedPreferences.getInstance();
  final themeStr = prefs.getString('theme');
  if (themeStr == 'dark') {
    themeNotifier.value = ThemeMode.dark;
  } else if (themeStr == 'light') {
    themeNotifier.value = ThemeMode.light;
  }

  // 최초 접속 여부 및 로그인 상태 확인
  final bool hasSeenOnboarding = prefs.getBool('hasSeenOnboarding') ?? false;
  final String? token = prefs.getString('eyeCatchToken');
  
  // 첫 화면 결정 로직
  String initialRoute = '/onboarding';
  if (hasSeenOnboarding) {
    if (token != null && token.isNotEmpty) {
      initialRoute = '/main'; // 온보딩도 봤고, 로그인도 되어있음
    } else {
      initialRoute = '/login'; // 온보딩은 봤지만, 로그인은 안됨
    }
  }

  runApp(EyeCatchApp(initialRoute: initialRoute));
}

class EyeCatchApp extends StatelessWidget {
  final String initialRoute;
  const EyeCatchApp({super.key, required this.initialRoute});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeNotifier,
      builder: (_, ThemeMode currentMode, __) {
        return MaterialApp(
          // navigatorKey: NotificationService.navigatorKey, 
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
          
          // 위에서 결정한 첫 화면으로 시작
          initialRoute: initialRoute, 
          routes: {
            '/onboarding': (context) => const OnboardingScreen(), // 온보딩 라우트 추가
            '/login': (context) => const LoginScreen(),
            '/main': (context) => const MainScreen(),
          },
        );
      },
    );
  }
}