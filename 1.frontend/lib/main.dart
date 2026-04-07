import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
// 🔥 구글 폰트 임포트 추가
import 'package:google_fonts/google_fonts.dart'; 

import 'screens/login_screen.dart';
import 'screens/main_screen.dart';

final ValueNotifier<ThemeMode> themeNotifier = ValueNotifier(ThemeMode.system);

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
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

          // 🔥 2. 라이트 테마에 폰트 적용
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: const Color(0xFF003d9b),
              brightness: Brightness.light,
            ),
            useMaterial3: true,
            // Noto Sans KR 폰트를 전체 텍스트 테마에 적용
            textTheme: GoogleFonts.notoSansKrTextTheme(
              Theme.of(context).textTheme,
            ),
          ),

          // 다크 테마에 폰트 적용
          darkTheme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: const Color(0xFF60a5fa),
              brightness: Brightness.dark,
            ),
            useMaterial3: true,
            // 다크 모드용 Noto Sans KR 적용 (글씨 색상 반전을 위해 ThemeData 밝기 지정)
            textTheme: GoogleFonts.notoSansKrTextTheme(
              ThemeData(brightness: Brightness.dark).textTheme,
            ),
          ),
          
          themeMode: currentMode,
          initialRoute: '/login',
          routes: {
            '/login': (context) => const LoginScreen(),
            '/main': (context) => const MainScreen(),
          },
        );
      },
    );
  }
}