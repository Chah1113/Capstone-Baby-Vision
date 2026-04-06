// src/pages/Main.jsx 전체 교체
import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function Main() {
  const navigate = useNavigate();
  const [userName, setUserName] = useState('');

  useEffect(() => {
    const savedUser = JSON.parse(localStorage.getItem('eyeCatchUser'));
    if (savedUser && savedUser.name) {
      setUserName(savedUser.name);
    } else {
      alert('로그인이 필요한 서비스입니다.');
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    alert('안전하게 로그아웃 되었습니다.');
    navigate('/login');
  };

  return (
    <div className="text-on-surface min-h-screen pb-28 bg-background font-body transition-colors duration-300">
      
      {/* 상단 헤더 */}
      <header className="bg-slate-50/70 dark:bg-slate-900/70 backdrop-blur-xl fixed top-0 w-full z-50 shadow-sm dark:shadow-none flex justify-between items-center px-6 py-4 transition-colors duration-300">
        <div className="flex items-center gap-3">
          {/* 아이콘을 좀 더 가정적인 느낌으로 (눈 -> 집/shield) */}
          <span className="material-symbols-outlined text-blue-700 dark:text-blue-400">home_pin</span>
          <h1 className="text-xl font-extrabold tracking-tighter text-blue-800 dark:text-blue-100 font-headline">Eye Catch</h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm font-bold text-on-surface-variant">{userName} 보호자님</span>
          <button onClick={handleLogout} className="text-xs bg-slate-200 dark:bg-slate-700 px-3 py-1.5 rounded hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors font-bold text-slate-700 dark:text-slate-200">로그아웃</button>
        </div>
      </header>

      <main className="pt-24 px-4 md:px-8 max-w-7xl mx-auto">
        <section className="mb-8 mt-4">
          <div className="flex justify-between items-end">
            <div>
              <p className="text-sm font-semibold text-primary mb-1 uppercase tracking-wider">우리 아이 안심 케어</p>
              <h2 className="text-3xl font-extrabold font-headline tracking-tight text-on-surface dark:text-white">실시간 아이방 상황</h2>
            </div>
          </div>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8 space-y-6">
            
            {/* 💡 수정한 부분: 아이방 썸네일 & 재생 버튼 */}
            <div 
              onClick={() => navigate('/live-stream')}
              className="relative aspect-video bg-slate-900 rounded-3xl overflow-hidden shadow-sm group cursor-pointer border border-slate-200 dark:border-slate-800"
            >
              {/* 공장 이미지 -> 아이방/거실 놀이방 이미지로 교체 */}
              <img 
                className="w-full h-full object-cover opacity-60 group-hover:opacity-40 transition-opacity duration-300" 
                src="https://images.unsplash.com/photo-1596131398991-b94f928d85a1?auto=format&fit=crop&q=80" 
                alt="아이방 베이비캠" 
              />
              
              {/* 중앙 재생 버튼 */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="bg-blue-600/90 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-all duration-300 backdrop-blur-sm">
                  <span className="material-symbols-outlined text-4xl ml-1">play_arrow</span>
                </div>
              </div>

              {/* 썸네일 내부 텍스트 수정 */}
              <div className="absolute inset-0 p-6 pointer-events-none flex flex-col justify-between">
                <div className="flex justify-end">
                  <div className="bg-black/50 backdrop-blur-md px-3 py-1 rounded-full flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    <span className="text-xs font-bold text-white">LIVE 연결됨</span>
                  </div>
                </div>
                <div>
                  <h3 className="text-white font-bold text-xl drop-shadow-md">거실 놀이방 베이비캠</h3>
                  <p className="text-slate-200 text-sm drop-shadow-md mt-1">터치하여 우리 아이 상태 확인</p>
                </div>
              </div>
            </div>

            {/* 최근 알림 카드 수정 (가정/아이 관련 에러로 변경) */}
            <Link to="/incident-details" className="block bg-surface-container-lowest dark:bg-slate-800 p-5 rounded-xl shadow-sm space-y-4 hover:shadow-md transition-shadow duration-300">
              <div className="flex justify-between items-center">
                <h3 className="text-sm font-bold font-headline text-on-surface dark:text-white uppercase tracking-wider">최근 아이 활동</h3>
                <span className="text-xs text-on-surface-variant font-medium">방금 전</span>
              </div>
              {/* 북측 창고 무단 접근 -> 움직임 감지/현관문 열림 등으로 변경 */}
              <div className="flex items-center gap-4 bg-surface-container-low dark:bg-slate-700 p-3 rounded-lg border-l-4 border-error transition-colors duration-300">
                <div className="w-16 h-12 rounded bg-slate-200 dark:bg-slate-600 overflow-hidden shrink-0 relative">
                  {/* 알림 이미지 -> 계단근처 아이/현관문 열리는 이미지로 교체 */}
                  <img src="https://images.unsplash.com/photo-1519689680058-324335c77eba?w=800&auto=format&fit=crop&q=80" className="w-full h-full object-cover" alt="알림 이미지" />
                </div>
                <div className="grow">
                  <p className="text-sm font-semibold text-error">아이방 움직임 감지 (주의)</p>
                  <p className="text-xs text-on-surface-variant">구역 1: 침대 주변</p>
                </div>
                <span className="material-symbols-outlined text-primary dark:text-blue-400">chevron_right</span>
              </div>
            </Link>
          </div>

          <div className="lg:col-span-4 space-y-6">
            {/* AI 현황 카드 -> 아이 안심 AI 지수로 문구 수정 */}
            <div className="bg-surface-container-lowest dark:bg-slate-800 p-6 rounded-3xl shadow-sm border border-slate-100 dark:border-slate-700 transition-colors duration-300">
              <h3 className="font-headline font-bold text-on-surface dark:text-white mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-primary dark:text-blue-400">child_care</span> 우리 아이 안심 AI
              </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-xs mb-1.5">
                    <span className="text-on-surface-variant font-medium">모니터링 정확도</span>
                    <span className="text-primary dark:text-blue-400 font-bold">98.2%</span>
                  </div>
                  <div className="h-1.5 w-full bg-surface-container-low dark:bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full bg-primary dark:bg-blue-500" style={{ width: '98.2%' }}></div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-3 bg-blue-50 dark:bg-slate-700/50 rounded-2xl transition-colors duration-300">
                  <span className="text-xs font-semibold text-blue-800 dark:text-blue-200">설정된 안심 구역</span>
                  <span className="text-lg font-headline font-extrabold text-blue-900 dark:text-blue-100">3개</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* 하단 네비게이션 바 수정 */}
      <nav className="fixed bottom-0 left-0 w-full flex justify-around items-center px-4 pb-4 pt-2 bg-white dark:bg-slate-800 shadow-[0_-4px_20px_rgba(0,0,0,0.05)] dark:shadow-none dark:border-t dark:border-slate-700 z-50 rounded-t-xl transition-colors duration-300">
        <Link to="/main" className="flex flex-col items-center justify-center bg-blue-50 dark:bg-blue-900/30 text-blue-800 dark:text-blue-100 rounded-2xl px-5 py-2 transition-all">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>videocam</span>
          <span className="text-xs font-medium">모니터링</span>
        </Link>
        <Link to="/zone" className="flex flex-col items-center justify-center text-slate-500 dark:text-slate-400 px-5 py-2 hover:text-blue-600 dark:hover:text-blue-300 transition-all">
          <span className="material-symbols-outlined">grid_view</span>
          <span className="text-xs font-medium">구역</span>
        </Link>
        <Link to="/history" className="flex flex-col items-center justify-center text-slate-500 dark:text-slate-400 px-5 py-2 hover:text-blue-600 dark:hover:text-blue-300 transition-all">
          <span className="material-symbols-outlined">warning</span>
          <span className="text-xs font-medium">사건 내역</span>
        </Link>
        <Link to="/settings" className="flex flex-col items-center justify-center text-slate-500 dark:text-slate-400 px-5 py-2 hover:text-blue-600 dark:hover:text-blue-300 transition-all">
          <span className="material-symbols-outlined">settings</span>
          <span className="text-xs font-medium">설정</span>
        </Link>
      </nav>
    </div>
  );
}

export default Main;