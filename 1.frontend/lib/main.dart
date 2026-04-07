import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
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

          // 🔥 수정됨: Theme.of(context) 대신 ThemeData.light() 객체 사용 (에러 방지)
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: const Color(0xFF003d9b),
              brightness: Brightness.light,
            ),
            useMaterial3: true,
            textTheme: GoogleFonts.notoSansKrTextTheme(
              ThemeData.light().textTheme,
            ),
          ),

          // 🔥 수정됨: Theme.of(context) 대신 ThemeData.dark() 객체 사용 (에러 방지)
          darkTheme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: const Color(0xFF60a5fa),
              brightness: Brightness.dark,
            ),
            useMaterial3: true,
            textTheme: GoogleFonts.notoSansKrTextTheme(
              ThemeData.dark().textTheme,
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