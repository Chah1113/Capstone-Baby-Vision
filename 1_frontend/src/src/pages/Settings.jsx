// src/pages/Settings.jsx 전체 교체
import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function Settings() {
  const navigate = useNavigate();
  const [profileName, setProfileName] = useState('보호자');
  const [profileEmail, setProfileEmail] = useState('parent@eyecatch.ai');
  
  // 토글 버튼들의 상태 관리
  const [isAlertOn, setIsAlertOn] = useState(true);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // 1. 프로필 이름 및 이메일 가져오기
    const savedUser = JSON.parse(localStorage.getItem('eyeCatchUser'));
    if (savedUser) {
      if (savedUser.name) setProfileName(savedUser.name);
      if (savedUser.email) setProfileEmail(savedUser.email);
    }

    // 2. 다크 모드 초기 상태 가져오기
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  const handleLogout = () => {
    alert('안전하게 로그아웃 되었습니다.');
    navigate('/login');
  };

  // 다크 모드 전환 함수
  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => {
      const newMode = !prevMode;
      if (newMode) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
      return newMode;
    });
  };

  return (
    <div className="text-on-surface min-h-screen pb-28 bg-background dark:bg-slate-900 font-body transition-colors duration-300">
      
      {/* 🌙 상단 헤더 */}
      <header className="fixed top-0 w-full z-50 bg-slate-50/70 dark:bg-slate-900/70 backdrop-blur-xl shadow-sm dark:shadow-none flex justify-between items-center px-6 py-4 transition-colors duration-300">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-blue-700 dark:text-blue-400">home_pin</span>
          <span className="text-xl font-extrabold tracking-tighter text-blue-800 dark:text-blue-300 font-headline">Eye Catch</span>
        </div>
        <div className="flex items-center gap-4">
          <button className="material-symbols-outlined text-slate-500 dark:text-slate-400 hover:opacity-80 transition-opacity">notifications</button>
          <div className="w-8 h-8 rounded-full overflow-hidden border border-outline-variant/30 flex items-center justify-center bg-slate-100 dark:bg-slate-700">
            <span className="material-symbols-outlined text-slate-400">person</span>
          </div>
        </div>
      </header>

      <main className="pt-24 px-6 max-w-4xl mx-auto space-y-8">
        {/* 👤 프로필 카드 영역 */}
        <section className="flex flex-col md:flex-row items-center md:items-start gap-8 bg-surface-container-lowest dark:bg-slate-800 p-8 rounded-[3rem] shadow-[0_4px_20px_rgba(0,24,72,0.04)] dark:shadow-none transition-colors duration-300">
          <div className="relative">
            {/* 산업용 느낌의 남성 이미지 -> 중립적인 가족/아동 아이콘으로 대체 권장 (현재는 언스플래쉬 중립 이미지로 교체) */}
            <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-primary-fixed dark:border-blue-900/50">
              <img alt="프로필" className="w-full h-full object-cover" src="https://images.unsplash.com/photo-1596131398991-b94f928d85a1?auto=format&fit=crop&q=80" />
            </div>
            <button className="absolute bottom-1 right-1 bg-primary text-on-primary p-2 rounded-full shadow-lg hover:scale-105 transition-transform">
              <span className="material-symbols-outlined text-sm">edit</span>
            </button>
          </div>
          
          <div className="flex-1 text-center md:text-left">
            <h1 className="text-3xl font-extrabold font-headline tracking-tight text-on-surface dark:text-white">{profileName} 보호자님</h1>
            {/* 맘앤대디 안심 계정*/}
            <p className="text-on-surface-variant dark:text-slate-400 font-medium mt-1">맘앤대디 안심 계정</p>
            <div className="mt-4 flex flex-wrap justify-center md:justify-start gap-2">
              <span className="px-3 py-1 bg-blue-50 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300 text-xs font-bold rounded-full">패밀리 리더</span>
              <span className="px-3 py-1 bg-surface-container-high dark:bg-slate-700 text-on-surface-variant dark:text-slate-300 text-xs font-bold rounded-full">관리자 권한</span>
            </div>
          </div>
          
          <div className="flex flex-col gap-3 w-full md:w-auto">
            <button onClick={handleLogout} className="text-white px-6 py-2.5 rounded-xl font-bold flex items-center justify-center gap-2 active:scale-95 transition-transform shadow-md" style={{ background: 'linear-gradient(135deg, #003d9b 0%, #0052cc 100%)' }}>
              <span className="material-symbols-outlined text-[20px]">logout</span> 로그아웃
            </button>
          </div>
        </section>

        {/* ⚙️ 설정 그리드 영역 */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          
          {/* 계정 관리 카드 */}
          <div className="bg-surface-container-lowest dark:bg-slate-800 p-6 rounded-4xl shadow-sm flex flex-col justify-between md:col-span-12 transition-colors duration-300">
            <div>
              <h3 className="text-lg font-bold font-headline mb-4 flex items-center gap-2 dark:text-white">
                <span className="material-symbols-outlined text-primary dark:text-blue-400">manage_accounts</span> 계정 관리
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-surface-container-low dark:bg-slate-700/50 rounded-xl hover:bg-surface-container-high dark:hover:bg-slate-700 transition-colors cursor-pointer">
                  <div>
                    <p className="text-xs text-on-surface-variant dark:text-slate-400 font-bold">보호자 정보 수정</p>
                    <p className="text-sm font-medium dark:text-white">{profileName}</p>
                  </div>
                  <span className="material-symbols-outlined text-slate-400">person</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-surface-container-low dark:bg-slate-700/50 rounded-xl">
                  <div>
                    <p className="text-xs text-on-surface-variant dark:text-slate-400 font-bold">비상 연락처 (이메일)</p>
                    <p className="text-sm font-medium dark:text-white">{profileEmail}</p>
                  </div>
                  <span className="material-symbols-outlined text-slate-400">chevron_right</span>
                </div>
              </div>
            </div>
          </div>

          {/* 환경 설정 카테고리 */}
          <div className="md:col-span-12 space-y-4">
            <h3 className="text-lg font-bold font-headline px-2 dark:text-white">아이 안심 환경 설정</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              
              {/* 1. 알림 및 경고 토글 */}
              <div onClick={() => setIsAlertOn(!isAlertOn)} className="bg-surface-container-lowest dark:bg-slate-800 p-5 rounded-4xl flex items-center justify-between hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors group cursor-pointer shadow-sm">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors ${isAlertOn ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400' : 'bg-slate-100 text-slate-500 dark:bg-slate-700'}`}>
                    <span className="material-symbols-outlined">{isAlertOn ? 'notifications_active' : 'notifications_off'}</span>
                  </div>
                  <div>
                    <p className="font-bold text-sm dark:text-white">아이 활동 알림</p>
                    <p className="text-xs text-on-surface-variant dark:text-slate-400">위험 구역 접근 및 울음소리 감지 시 즉시 알림</p>
                  </div>
                </div>
                <div className={`w-12 h-7 rounded-full relative flex items-center px-1 transition-colors duration-300 ${isAlertOn ? 'bg-primary dark:bg-blue-600' : 'bg-slate-300 dark:bg-slate-600'}`}>
                  <div className={`w-5 h-5 bg-white rounded-full shadow-sm transform transition-transform duration-300 ${isAlertOn ? 'translate-x-5' : 'translate-x-0'}`}></div>
                </div>
              </div>

              {/* 2. 다크 모드 토글 */}
              <div onClick={toggleDarkMode} className="bg-surface-container-lowest dark:bg-slate-800 p-5 rounded-4xl flex items-center justify-between hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors group cursor-pointer shadow-sm">
                <div className="flex items-center gap-4">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors ${isDarkMode ? 'bg-indigo-50 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-400' : 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300'}`}>
                    <span className="material-symbols-outlined">{isDarkMode ? 'dark_mode' : 'light_mode'}</span>
                  </div>
                  <div>
                    <p className="font-bold text-sm dark:text-white">야간 모드 (다크)</p>
                    <p className="text-xs text-on-surface-variant dark:text-slate-400">어두운 방에서 모니터링 시 눈 보호</p>
                  </div>
                </div>
                <div className={`w-12 h-7 rounded-full relative flex items-center px-1 transition-colors duration-300 ${isDarkMode ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-600'}`}>
                  <div className={`w-5 h-5 bg-white rounded-full shadow-sm transform transition-transform duration-300 ${isDarkMode ? 'translate-x-5' : 'translate-x-0'}`}></div>
                </div>
              </div>

              {/* 3. 언어 설정 */}
              <div className="bg-surface-container-lowest dark:bg-slate-800 p-5 rounded-4xl flex items-center justify-between hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors group cursor-pointer shadow-sm">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-slate-700 dark:text-slate-300">
                    <span className="material-symbols-outlined">language</span>
                  </div>
                  <div>
                    <p className="font-bold text-sm dark:text-white">앱 언어 설정</p>
                    <p className="text-xs text-on-surface-variant dark:text-slate-400">한국어 (Korean)</p>
                  </div>
                </div>
                <span className="material-symbols-outlined text-slate-300 dark:text-slate-500">chevron_right</span>
              </div>

              {/* 4. 성장 기록 및 추억 저장소 */}
              <div className="bg-surface-container-lowest dark:bg-slate-800 p-5 rounded-4xl flex items-center justify-between hover:bg-surface-container-low dark:hover:bg-slate-700 transition-colors group cursor-pointer shadow-sm">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-slate-700 dark:text-slate-300">
                    <span className="material-symbols-outlined">favorite</span>
                  </div>
                  <div>
                    <p className="font-bold text-sm dark:text-white">성장 기록 및 추억 저장소</p>
                    <p className="text-xs text-on-surface-variant dark:text-slate-400">감지된 활동 영상 90일 보관</p>
                  </div>
                </div>
                <span className="material-symbols-outlined text-slate-300 dark:text-slate-500">chevron_right</span>
              </div>

            </div>
          </div>

          {/* 푸터 링크 */}
          <div className="md:col-span-12 flex justify-center gap-8 py-8">
            <a className="text-xs text-on-surface-variant dark:text-slate-500 hover:text-primary dark:hover:text-blue-400 underline decoration-slate-200 dark:decoration-slate-700 underline-offset-4" href="#">서비스 이용약관</a>
            <a className="text-xs text-on-surface-variant dark:text-slate-500 hover:text-primary dark:hover:text-blue-400 underline decoration-slate-200 dark:decoration-slate-700 underline-offset-4" href="#">개인정보 처리방침</a>
            <a className="text-xs text-on-surface-variant dark:text-slate-500 hover:text-primary dark:hover:text-blue-400 underline decoration-slate-200 dark:decoration-slate-700 underline-offset-4" href="#">고객 센터</a>
          </div>
        </div>
      </main>

      {/* 하단 네비게이션 */}
      <nav className="fixed bottom-0 left-0 w-full flex justify-around items-center px-4 pb-4 pt-2 bg-white dark:bg-slate-800 shadow-[0_-4px_20px_rgba(0,0,0,0.05)] dark:shadow-none dark:border-t dark:border-slate-700 z-50 rounded-t-xl transition-colors duration-300">
        <Link to="/main" className="flex flex-col items-center justify-center text-slate-500 dark:text-slate-400 px-5 py-2 hover:text-blue-600 dark:hover:text-blue-300 transition-all">
          <span className="material-symbols-outlined">videocam</span>
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
        <Link to="/settings" className="flex flex-col items-center justify-center bg-blue-50 dark:bg-blue-900/30 text-blue-800 dark:text-blue-100 rounded-2xl px-5 py-2 transition-all">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>settings</span>
          <span className="text-xs font-medium">설정</span>
        </Link>
      </nav>
    </div>
  );
}

export default Settings;