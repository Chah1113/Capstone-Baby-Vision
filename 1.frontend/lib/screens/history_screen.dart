import 'package:flutter/material.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> with SingleTickerProviderStateMixin {
  bool _isLoading = true;
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    // 깜빡임(Pulse) 효과 애니메이션 컨트롤러
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    )..repeat(reverse: true);

    // 실제 API 호출 대신 1.5초 대기로 로딩 시뮬레이션
    Future.delayed(const Duration(milliseconds: 1500), () {
      if (mounted) setState(() => _isLoading = false);
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      appBar: AppBar(
        title: Text('Eye Catch',
            style: TextStyle(fontWeight: FontWeight.bold, color: Theme.of(context).colorScheme.primary)),
        elevation: 0,
        backgroundColor: Colors.transparent,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '우리 아이 안심 로그',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            
            // 로딩 상태에 따라 스켈레톤 UI 또는 실제 로그 카드 렌더링
            _isLoading ? _buildSkeletonCard() : _buildLogCard(context),
          ],
        ),
      ),
    );
  }

  // 로딩 스켈레톤 UI
  Widget _buildSkeletonCard() {
    final baseColor = Theme.of(context).colorScheme.surfaceContainerHighest;

    return AnimatedBuilder(
      animation: _pulseController,
      builder: (context, child) {
        return Opacity(
          opacity: 0.5 + (_pulseController.value * 0.5), // 0.5 ~ 1.0 사이로 깜빡임
          child: Container(
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              borderRadius: BorderRadius.circular(16),
            ),
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  height: 160,
                  width: double.infinity,
                  decoration: BoxDecoration(color: baseColor, borderRadius: BorderRadius.circular(12)),
                ),
                const SizedBox(height: 16),
                Container(height: 14, width: 80, color: baseColor),
                const SizedBox(height: 8),
                Container(height: 20, width: 200, color: baseColor),
                const SizedBox(height: 8),
                Container(height: 14, width: 150, color: baseColor),
                const SizedBox(height: 16),
                Container(height: 48, width: double.infinity, decoration: BoxDecoration(color: baseColor, borderRadius: BorderRadius.circular(8))),
              ],
            ),
          ),
        );
      },
    );
  }

  // 실제 로그 카드 (기존과 동일하되 Theme 적용)
  Widget _buildLogCard(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Theme.of(context).shadowColor.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: Image.network(
                    'https://images.unsplash.com/photo-1519689680058-324335c77eba?w=800&auto=format&fit=crop&q=80',
                    height: 160,
                    width: double.infinity,
                    fit: BoxFit.cover,
                  ),
                ),
                Positioned(
                  top: 12, left: 12,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primary,
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Text('AI 탐지', style: TextStyle(color: Theme.of(context).colorScheme.onPrimary, fontSize: 10, fontWeight: FontWeight.bold)),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Text('움직임 감지 (주의)', style: TextStyle(color: Colors.redAccent, fontSize: 12, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            const Text('계단 위험 구역 접근', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text('2026년 4월 4일 오후 5:45', style: TextStyle(color: Theme.of(context).colorScheme.onSurfaceVariant, fontSize: 14)),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/incident-details'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  foregroundColor: Theme.of(context).colorScheme.onPrimary,
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
                child: const Text('상세 기록 확인', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}